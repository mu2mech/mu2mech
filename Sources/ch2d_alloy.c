/*
 * ch2d_alloy.c — 2-D Cahn-Hilliard solver for a binary alloy with
 * thermodynamic Gibbs free energy from CALPHAD coefficients.
 *
 * Free energy density (non-dimensionalised):
 *   g(c) = Ag * (aa·c⁴ + bb·c³ + cc·c² + dd·c + ee)
 *   μ(c) = dg/dc = Ag * (4aa·c³ + 3bb·c² + 2cc·c + dd)
 *
 * Mobility:  M(c) = c(1-c)   (degenerate, vanishes at pure phases)
 *
 * Time integration: semi-implicit spectral with degenerate mobility
 * (Zhu–Chen–Shen scheme):
 *
 *   flux_x̂(t+Δt) = ik_x [ μ̂(t) + κ·k²·ĉ(t) ]     (Fourier of  M·∂μ̂/∂x )
 *   ĉ(t+Δt) = [ (1 + 0.5Δt·k⁴)·ĉ(t)
 *               + Δt·i(k_x·f̂₂ₓ + k_y·f̂₂ᵧ) ]
 *             / (1 + 0.5Δt·k⁴)
 *
 * where f₂ = M(c)·(IFFT of ik·[μ̂ + κk²ĉ]) and gradient energy κ = Hg.
 *
 * Spinodal points pp1, pp2 are the inflection points of g(c):
 *   pp₁,₂ = (-6bb ± √(36bb²-96aa·cc)) / 24aa
 *
 * Regions:
 *   c_avg outside [pp2, pp1]  →  metastable/stable  (nucleation)
 *   c_avg inside  [pp2, pp1]  →  unstable            (spinodal decomposition)
 *
 * Input file (input.dat):
 *   aa … ee       Gibbs polynomial coefficients
 *   Ag            energy scale
 *   Hg            barrier height (gradient energy coefficient)
 *   fluctuation   noise amplitude
 *   cAvg          mean composition
 *   lx, ly        grid dimensions
 *   delT          time step
 *   delX, delY    grid spacings
 *   timeInterval  output interval
 *   totalTime     end time
 *   resume        0 = fresh, 1 = resume
 *   resumeFrom    resume time (as string matching filename)
 */

#include "ch_common.h"
#include "nrutil.c"
#include "gasdev.c"

/* ── Input parameters ─────────────────────────────────────────────────────── */
typedef struct {
    double aa, bb, cc, dd, ee;  /* Gibbs polynomial coefficients          */
    double Ag;                   /* energy scale                           */
    double Hg;                   /* barrier height / gradient coefficient  */
    double fluctuation;          /* noise amplitude                        */
    double c_avg;                /* mean composition                       */
    int    grid_x, grid_y;       /* grid dimensions                        */
    double dt;                   /* time step                              */
    double dx, dy;               /* grid spacings                          */
    double save_interval;        /* output interval                        */
    double total_time;           /* end time                               */
    int    resume;               /* 0 = fresh, 1 = resume                 */
    char   resume_from_str[32];  /* resume time as string                 */
    double resume_from;          /* resume time as double                 */
} AlloySim2D;

static void read_params(AlloySim2D *p)
{
    KVDoc doc         = kv_load("input.dat");
    p->aa             = kv_get_double(&doc, "aa");
    p->bb             = kv_get_double(&doc, "bb");
    p->cc             = kv_get_double(&doc, "cc");
    p->dd             = kv_get_double(&doc, "dd");
    p->ee             = kv_get_double(&doc, "ee");
    p->Ag             = kv_get_double(&doc, "Ag");
    p->Hg             = kv_get_double(&doc, "Hg");
    p->fluctuation    = kv_get_double(&doc, "fluctuation");
    p->c_avg          = kv_get_double(&doc, "cAvg");
    p->grid_x         = kv_get_int   (&doc, "lx");
    p->grid_y         = kv_get_int   (&doc, "ly");
    p->dt             = kv_get_double(&doc, "delT");
    p->dx             = kv_get_double(&doc, "delX");
    p->dy             = kv_get_double(&doc, "delY");
    p->save_interval  = kv_get_double(&doc, "timeInterval");
    p->total_time     = kv_get_double(&doc, "totalTime");
    p->resume         = kv_get_int   (&doc, "resume");
    kv_get_string(&doc, "resumeFrom", p->resume_from_str, sizeof(p->resume_from_str));
    sscanf(p->resume_from_str, "%lf", &p->resume_from);
}

/*
 * Non-dimensionalised chemical potential  dg/dc, scaled by Ag/Hg.
 * Hg (barrier height) acts as an energy normalisation so the time step
 * Δt and grid spacing remain stable for typical alloy coefficients.
 */
static inline double chem_potential(const AlloySim2D *p, double c)
{
    return (p->Ag / p->Hg) * (4.0*p->aa*c*c*c + 3.0*p->bb*c*c + 2.0*p->cc*c + p->dd);
}

/* ── Degenerate mobility  M(c) = c(1-c) ──────────────────────────────────── */
static inline double mobility(double c) { return c * (1.0 - c); }

/*
 * Add zero-mean Gaussian thermal noise to the composition field.
 * Four independent noise arrays are generated, scaled, mean-subtracted, and
 * added — this was the approach in the original code and is preserved.
 *
 * 'seeds' must point to an array of 4 long ints that persist between calls
 * so the RNG state evolves across time steps.
 */
static void add_thermal_noise(fftw_complex *composition,
                              int lx, int ly,
                              double noise_scale,
                              long seeds[4])
{
    float gasdev(long *idum);
    double **noise = dmatrix(0, lx, 0, ly);
    double rsum, rmean;

    for (int pass = 0; pass < 4; pass++) {
        /* Fill noise array with Gaussian samples, then mean-subtract */
        rsum = 0.0;
        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++) {
                noise[i][j] = gasdev(&seeds[pass]) * noise_scale;
                rsum += noise[i][j];
            }
        rmean = rsum / (double)(lx * ly);

        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++)
                composition[IDX2(i, j, ly)] += noise[i][j] - rmean;
    }
    free_dmatrix(noise, 0, lx, 0, ly);
}

/* ── Main ─────────────────────────────────────────────────────────────────── */
int main(void)
{
    AlloySim2D p;
    read_params(&p);

    int lx = p.grid_x;
    int ly = p.grid_y;
    int n_total = lx * ly;

    /* Spinodal inflection points of g(c) */
    double discriminant = 36.0*p.bb*p.bb - 96.0*p.aa*p.cc;
    double pp1 = (-6.0*p.bb + sqrt(discriminant)) / (24.0*p.aa);
    double pp2 = (-6.0*p.bb - sqrt(discriminant)) / (24.0*p.aa);
    if (pp1 < pp2) { double tmp = pp1; pp1 = pp2; pp2 = tmp; } /* pp1 > pp2 */

    int inside_spinodal = (p.c_avg >= pp2 && p.c_avg <= pp1);

    /* ── FFTW allocations ─────────────────────────────────────────────────── */
    fftw_complex *composition        = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *composition_hat    = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *mu_field           = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *mu_hat             = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *mobility_field     = fftw_malloc(sizeof(fftw_complex) * n_total);
    /* flux = M · IFFT(ik·[μ̂ + κk²ĉ]),  computed per direction */
    fftw_complex *flux_work_hat_x    = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *flux_work_hat_y    = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *flux_work_x        = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *flux_work_y        = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *weighted_flux_x    = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *weighted_flux_y    = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *weighted_flux_hat_x= fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *weighted_flux_hat_y= fftw_malloc(sizeof(fftw_complex) * n_total);

    if (!composition || !composition_hat || !mu_field || !mu_hat ||
        !mobility_field || !flux_work_hat_x || !flux_work_hat_y ||
        !flux_work_x || !flux_work_y || !weighted_flux_x || !weighted_flux_y ||
        !weighted_flux_hat_x || !weighted_flux_hat_y) {
        fprintf(stderr, "ERROR: FFTW allocation failed\n");
        return EXIT_FAILURE;
    }

    /* FFT plans */
    fftw_plan plan_fwd_c    = fftw_plan_dft_2d(lx, ly, composition,        composition_hat,     FFTW_FORWARD,  FFTW_ESTIMATE);
    fftw_plan plan_fwd_mu   = fftw_plan_dft_2d(lx, ly, mu_field,           mu_hat,              FFTW_FORWARD,  FFTW_ESTIMATE);
    fftw_plan plan_bwd_c    = fftw_plan_dft_2d(lx, ly, composition_hat,    composition,         FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_plan plan_bwd_fx   = fftw_plan_dft_2d(lx, ly, flux_work_hat_x,    flux_work_x,         FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_plan plan_bwd_fy   = fftw_plan_dft_2d(lx, ly, flux_work_hat_y,    flux_work_y,         FFTW_BACKWARD, FFTW_ESTIMATE);
    fftw_plan plan_fwd_wfx  = fftw_plan_dft_2d(lx, ly, weighted_flux_x,    weighted_flux_hat_x, FFTW_FORWARD,  FFTW_ESTIMATE);
    fftw_plan plan_fwd_wfy  = fftw_plan_dft_2d(lx, ly, weighted_flux_y,    weighted_flux_hat_y, FFTW_FORWARD,  FFTW_ESTIMATE);

    /* ── Initial condition ────────────────────────────────────────────────── */
    if (p.resume == 0) {
        /* Initialise to c_avg */
        for (int n = 0; n < n_total; n++)
            composition[n] = p.c_avg;

        /* Add noise appropriate to the thermodynamic region */
        if (inside_spinodal) {
            /* Spinodal: small uniform noise sufficient to trigger decomposition */
            for (int i = 0; i < lx; i++)
                for (int j = 0; j < ly; j++)
                    composition[IDX2(i, j, ly)] +=
                        (-1.0 + 2.0*((double)rand()/(double)RAND_MAX)) / 200.0;
        } else {
            /*
             * Nucleation regime: larger Gaussian noise to provide nuclei.
             * Seeds are negative to initialise the NR RNG from scratch.
             */
            long seeds[4] = { -949L, -819L, -16L, -49L };
            add_thermal_noise(composition, lx, ly, 0.005, seeds);
            /* Additional uniform perturbation on top */
            for (int i = 0; i < lx; i++)
                for (int j = 0; j < ly; j++)
                    composition[IDX2(i, j, ly)] +=
                        (-1.0 + 2.0*((double)rand()/(double)RAND_MAX)) / 10.0;
        }
    } else {
        char resume_path[80];
        snprintf(resume_path, sizeof(resume_path),
                 "Output/Data/output_%s.dat", p.resume_from_str);
        load_field_2d(composition, lx, ly, resume_path);
    }

    /*
     * In the nucleation regime the sign of the driving force is flipped:
     * outside the spinodal the gradient of g pushes towards phase separation
     * only if it is used with the correct sign in the flux.
     * sign_mu = +1 inside spinodal, -1 outside spinodal.
     */
    double sign_mu = inside_spinodal ? 1.0 : -1.0;

    /*
     * Persistent RNG seeds for in-loop thermal noise.
     * Negative values initialise the NR generator; they evolve every call.
     */
    long noise_seeds[4] = { -949L, -819L, -16L, -49L };
    /* Thermal noise is added only for the first 1000 steps in nucleation mode */
    int noise_steps = inside_spinodal ? 0 : 1000;

    /* ── Time integration ─────────────────────────────────────────────────── */
    int step_start = (int)round(p.resume_from / p.dt);
    int step_end   = (int)round(p.total_time  / p.dt);

    for (int step = 1; step <= step_end; step++) {
        double time = step * p.dt;

        /* Compute chemical potential and mobility at every grid point */
        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++) {
                double c_val = creal(composition[IDX2(i, j, ly)]);
                mu_field[IDX2(i, j, ly)]       = sign_mu * chem_potential(&p, c_val);
                mobility_field[IDX2(i, j, ly)] = mobility(c_val);
            }

        /* Forward FFT of composition and chemical potential */
        fftw_execute(plan_fwd_mu);
        fftw_execute(plan_fwd_c);

        /*
         * Build  ik·[μ̂ + κk²ĉ]  in each direction.
         * κ is absorbed into Hg (barrier height sets the interface width).
         */
        for (int i = 0; i < lx; i++) {
            double kx  = kfreq(i, lx, p.dx);
            double kx2 = kx * kx;
            for (int j = 0; j < ly; j++) {
                double ky  = kfreq(j, ly, p.dy);
                double ky2 = ky * ky;
                double k2  = kx2 + ky2;
                int    idx = IDX2(i, j, ly);
                fftw_complex driving = mu_hat[idx] + k2 * composition_hat[idx];
                flux_work_hat_x[idx] = _Complex_I * kx * driving;
                flux_work_hat_y[idx] = _Complex_I * ky * driving;
            }
        }

        /* IFFT of fluxes → real-space flux components */
        fftw_execute(plan_bwd_fx);
        fftw_execute(plan_bwd_fy);

        /* Normalise and multiply by degenerate mobility M(c) */
        double inv_n = 1.0 / (double)n_total;
        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++) {
                int idx = IDX2(i, j, ly);
                double M = creal(mobility_field[idx]);
                weighted_flux_x[idx] = creal(flux_work_x[idx]) * inv_n * M;
                weighted_flux_y[idx] = creal(flux_work_y[idx]) * inv_n * M;
            }

        /* Forward FFT of mobility-weighted fluxes */
        fftw_execute(plan_fwd_wfx);
        fftw_execute(plan_fwd_wfy);

        /*
         * Semi-implicit Crank-Nicolson update:
         *   ĉ(t+Δt) = [ (1 + 0.5Δt·k⁴)·ĉ(t)
         *               + Δt·i(k_x·f̂₂ₓ + k_y·f̂₂ᵧ) ]
         *             / (1 + 0.5Δt·k⁴)
         */
        for (int i = 0; i < lx; i++) {
            double kx  = kfreq(i, lx, p.dx);
            double kx2 = kx * kx;
            for (int j = 0; j < ly; j++) {
                double ky  = kfreq(j, ly, p.dy);
                double ky2 = ky * ky;
                double k2  = kx2 + ky2;
                double k4  = k2 * k2;
                int    idx = IDX2(i, j, ly);
                double stabiliser = 0.5 * p.dt * k4;
                fftw_complex flux_div =
                    _Complex_I * (kx * weighted_flux_hat_x[idx]
                                + ky * weighted_flux_hat_y[idx]);
                composition_hat[idx] =
                    ((1.0 + stabiliser) * composition_hat[idx] + p.dt * flux_div)
                    / (1.0 + stabiliser);
            }
        }

        /* Inverse FFT back to real space */
        fftw_execute(plan_bwd_c);

        /* Normalise */
        for (int n = 0; n < n_total; n++)
            composition[n] *= inv_n;

        /* Thermal noise injection during early steps in nucleation regime */
        if (step <= noise_steps)
            add_thermal_noise(composition, lx, ly, 0.005, noise_seeds);

        /* Save output */
        if (should_save(step, p.dt, p.save_interval))
            save_field_2d(composition, lx, ly, time);
    }

    /* ── Cleanup ──────────────────────────────────────────────────────────── */
    fftw_destroy_plan(plan_fwd_c);
    fftw_destroy_plan(plan_fwd_mu);
    fftw_destroy_plan(plan_bwd_c);
    fftw_destroy_plan(plan_bwd_fx);
    fftw_destroy_plan(plan_bwd_fy);
    fftw_destroy_plan(plan_fwd_wfx);
    fftw_destroy_plan(plan_fwd_wfy);

    fftw_free(composition);
    fftw_free(composition_hat);
    fftw_free(mu_field);
    fftw_free(mu_hat);
    fftw_free(mobility_field);
    fftw_free(flux_work_hat_x);
    fftw_free(flux_work_hat_y);
    fftw_free(flux_work_x);
    fftw_free(flux_work_y);
    fftw_free(weighted_flux_x);
    fftw_free(weighted_flux_y);
    fftw_free(weighted_flux_hat_x);
    fftw_free(weighted_flux_hat_y);
    fftw_cleanup();

    return EXIT_SUCCESS;
}
