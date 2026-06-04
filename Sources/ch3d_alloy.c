/*
 * ch3d_alloy.c — 3-D Cahn-Hilliard solver for a binary alloy.
 *
 * Physics is identical to ch2d_alloy.c — see that file for free-energy and
 * mobility definitions.  The spectral update here uses a simpler constant
 * mobility M = 1 (the degenerate-mobility flux is more expensive in 3-D and
 * was not used in the original implementation).
 *
 * Semi-implicit update (M=1):
 *   ĉ(t+Δt) = [ ĉ(t) + Δt · k² · μ̂(t) ]
 *             / [ 1 + Δt · k⁴ ]
 *
 * Layout convention throughout:
 *   flat index of grid point (i, j, k)  =  i*(ly*lz) + j*lz + k
 * This matches FFTW's row-major 3-D convention for fftw_plan_dft_3d(lx,ly,lz).
 *
 * Input file (input.dat):
 *   aa … ee         Gibbs polynomial coefficients
 *   fluctuation     noise amplitude
 *   cAvg            mean composition
 *   lx, ly, lz      grid dimensions
 *   delT            time step
 *   delX, delY, delZ grid spacings
 *   timeInterval    output interval
 *   totalTime       end time
 *   resume          0 = fresh, 1 = resume
 *   resumeFrom      resume time (as string matching filename)
 */

#include "ch_common.h"
#include "nrutil.c"
#include "gasdev.c"

/* ── Input parameters ─────────────────────────────────────────────────────── */
typedef struct {
    double aa, bb, cc, dd, ee; /* Gibbs polynomial coefficients   */
    double fluctuation;         /* noise amplitude                 */
    double c_avg;               /* mean composition                */
    int    grid_x, grid_y, grid_z; /* grid dimensions             */
    double dt;                  /* time step                       */
    double dx, dy, dz;          /* grid spacings                   */
    double save_interval;       /* output interval                 */
    double total_time;          /* end time                        */
    int    resume;              /* 0 = fresh, 1 = resume           */
    char   resume_from_str[32]; /* resume time as string           */
    double resume_from;         /* resume time as double           */
} AlloySim3D;

static void read_params(AlloySim3D *p)
{
    KVDoc doc         = kv_load("input.dat");
    p->aa             = kv_get_double(&doc, "aa");
    p->bb             = kv_get_double(&doc, "bb");
    p->cc             = kv_get_double(&doc, "cc");
    p->dd             = kv_get_double(&doc, "dd");
    p->ee             = kv_get_double(&doc, "ee");
    p->fluctuation    = kv_get_double(&doc, "fluctuation");
    p->c_avg          = kv_get_double(&doc, "cAvg");
    p->grid_x         = kv_get_int   (&doc, "lx");
    p->grid_y         = kv_get_int   (&doc, "ly");
    p->grid_z         = kv_get_int   (&doc, "lz");
    p->dt             = kv_get_double(&doc, "delT");
    p->dx             = kv_get_double(&doc, "delX");
    p->dy             = kv_get_double(&doc, "delY");
    p->dz             = kv_get_double(&doc, "delZ");
    p->save_interval  = kv_get_double(&doc, "timeInterval");
    p->total_time     = kv_get_double(&doc, "totalTime");
    p->resume         = kv_get_int   (&doc, "resume");
    kv_get_string(&doc, "resumeFrom", p->resume_from_str, sizeof(p->resume_from_str));
    sscanf(p->resume_from_str, "%lf", &p->resume_from);
}

/* ── dg/dc = 4aa·c³ + 3bb·c² + 2cc·c + dd ───────────────────────────────── */
static inline double gibbs_deriv(const AlloySim3D *p, double c)
{
    return 4.0*p->aa*c*c*c + 3.0*p->bb*c*c + 2.0*p->cc*c + p->dd;
}

/*
 * Add zero-mean Gaussian thermal noise (4 independent passes, mean-subtracted).
 * 'seeds' must persist across calls so the RNG evolves between time steps.
 */
static void add_thermal_noise_3d(fftw_complex *composition,
                                 int lx, int ly, int lz,
                                 double noise_scale,
                                 long seeds[4])
{
    float gasdev(long *idum);
    double **noise_xy = dmatrix(0, lx, 0, ly);

    for (int pass = 0; pass < 4; pass++) {
        double rsum = 0.0;
        /* Generate 2-D noise slice (same amplitude applied in z) */
        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++) {
                noise_xy[i][j] = gasdev(&seeds[pass]) * noise_scale;
                rsum += noise_xy[i][j] * lz; /* total sum over all z */
            }
        double rmean = rsum / (double)(lx * ly * lz);

        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++)
                for (int k = 0; k < lz; k++)
                    composition[IDX3(i, j, k, ly, lz)] +=
                        noise_xy[i][j] - rmean;
    }
    free_dmatrix(noise_xy, 0, lx, 0, ly);
}

/* ── Main ─────────────────────────────────────────────────────────────────── */
int main(void)
{
    AlloySim3D p;
    read_params(&p);

    int lx = p.grid_x;
    int ly = p.grid_y;
    int lz = p.grid_z;
    int n_total = lx * ly * lz;

    /* Spinodal inflection points */
    double discriminant = 36.0*p.bb*p.bb - 96.0*p.aa*p.cc;
    double pp1 = (-6.0*p.bb + sqrt(discriminant)) / (24.0*p.aa);
    double pp2 = (-6.0*p.bb - sqrt(discriminant)) / (24.0*p.aa);
    if (pp1 < pp2) { double tmp = pp1; pp1 = pp2; pp2 = tmp; }

    int inside_spinodal = (p.c_avg >= pp2 && p.c_avg <= pp1);

    /* ── FFTW allocations ─────────────────────────────────────────────────── */
    fftw_complex *composition     = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *composition_hat = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *chem_pot        = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *chem_pot_hat    = fftw_malloc(sizeof(fftw_complex) * n_total);

    if (!composition || !composition_hat || !chem_pot || !chem_pot_hat) {
        fprintf(stderr, "ERROR: FFTW allocation failed\n");
        return EXIT_FAILURE;
    }

    /*
     * FFTW 3-D plan layout:  fftw_plan_dft_3d(n0, n1, n2, …) stores element
     * [i][j][k] at flat index i*n1*n2 + j*n2 + k, which matches IDX3(i,j,k,ly,lz).
     */
    fftw_plan plan_fwd_c   = fftw_plan_dft_3d(lx, ly, lz, composition,     composition_hat, FFTW_FORWARD,  FFTW_ESTIMATE);
    fftw_plan plan_fwd_mu  = fftw_plan_dft_3d(lx, ly, lz, chem_pot,        chem_pot_hat,    FFTW_FORWARD,  FFTW_ESTIMATE);
    fftw_plan plan_bwd_c   = fftw_plan_dft_3d(lx, ly, lz, composition_hat, composition,     FFTW_BACKWARD, FFTW_ESTIMATE);

    /* ── Initial condition ────────────────────────────────────────────────── */
    if (p.resume == 0) {
        /* Uniform mean composition */
        for (int n = 0; n < n_total; n++)
            composition[n] = p.c_avg;

        if (inside_spinodal) {
            /* Spinodal: small uniform noise to seed decomposition */
            for (int i = 0; i < lx; i++)
                for (int j = 0; j < ly; j++)
                    for (int k = 0; k < lz; k++)
                        composition[IDX3(i, j, k, ly, lz)] +=
                            (-1.0 + 2.0*((double)rand()/(double)RAND_MAX)) / 200.0;
        } else {
            /* Nucleation regime: Gaussian noise to provide nuclei */
            long seeds[4] = { -949L, -819L, -16L, -49L };
            add_thermal_noise_3d(composition, lx, ly, lz, 0.005, seeds);
        }
    } else {
        char resume_path[80];
        snprintf(resume_path, sizeof(resume_path),
                 "Output/Data/output_%s.dat", p.resume_from_str);
        load_field_3d(composition, lx, ly, lz, resume_path);
    }

    /* Sign of the driving force (same logic as ch2d_alloy) */
    double sign_mu = inside_spinodal ? -1.0 : 1.0;

    /* Persistent RNG seeds for in-loop noise injection */
    long noise_seeds[4] = { -949L, -819L, -16L, -49L };
    int noise_steps = inside_spinodal ? 0 : 1000;

    /* ── Time integration ─────────────────────────────────────────────────── */
    int step_start = (int)round(p.resume_from / p.dt);
    int step_end   = (int)round(p.total_time  / p.dt);

    for (int step = 1; step <= step_end; step++) {
        double time = step * p.dt;

        /* Compute df/dc at every grid point */
        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++)
                for (int k = 0; k < lz; k++) {
                    int idx = IDX3(i, j, k, ly, lz);
                    chem_pot[idx] = sign_mu * gibbs_deriv(&p, creal(composition[idx]));
                }

        /* Forward FFT of composition and chemical potential */
        fftw_execute(plan_fwd_mu);
        fftw_execute(plan_fwd_c);

        /*
         * Semi-implicit update with M=1:
         *   ĉ(t+Δt) = [ ĉ(t) + Δt·k²·μ̂(t) ] / [ 1 + Δt·k⁴ ]
         *
         * Using IDX3 ensures the flat index matches what FFTW produced.
         */
        for (int i = 0; i < lx; i++) {
            double kx  = kfreq(i, lx, p.dx);
            double kx2 = kx * kx;
            for (int j = 0; j < ly; j++) {
                double ky  = kfreq(j, ly, p.dy);
                double ky2 = ky * ky;
                for (int k = 0; k < lz; k++) {
                    double kz  = kfreq(k, lz, p.dz);
                    double kz2 = kz * kz;
                    double k2  = kx2 + ky2 + kz2;
                    double k4  = k2 * k2;
                    int    idx = IDX3(i, j, k, ly, lz);
                    composition_hat[idx] =
                        (composition_hat[idx] + p.dt * k2 * chem_pot_hat[idx])
                        / (1.0 + p.dt * k4);
                }
            }
        }

        /* Inverse FFT back to real space */
        fftw_execute(plan_bwd_c);

        /* Normalise */
        double inv_n = 1.0 / (double)n_total;
        for (int n = 0; n < n_total; n++)
            composition[n] *= inv_n;

        /* Thermal noise injection during early steps */
        if (step <= noise_steps)
            add_thermal_noise_3d(composition, lx, ly, lz, 0.005, noise_seeds);

        /* Save output */
        if (should_save(step, p.dt, p.save_interval))
            save_field_3d(composition, lx, ly, lz, time);
    }

    /* ── Cleanup ──────────────────────────────────────────────────────────── */
    fftw_destroy_plan(plan_fwd_c);
    fftw_destroy_plan(plan_fwd_mu);
    fftw_destroy_plan(plan_bwd_c);
    fftw_free(composition);
    fftw_free(composition_hat);
    fftw_free(chem_pot);
    fftw_free(chem_pot_hat);
    fftw_cleanup();

    return EXIT_SUCCESS;
}
