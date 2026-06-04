/*
 * ch2d_qualitative.c — 2-D Cahn-Hilliard solver with a qualitative double-well
 * free energy.
 *
 * Free energy density:  f(c) = c²(1-c)²
 *   => df/dc = 2c(1-c)(2c-1)
 *            = -2c(1 + 2c² - 3c)       (form used below)
 *
 * Time integration: semi-implicit spectral (Eyre splitting):
 *   ĉ(t+Δt) = [ ĉ(t) + Δt · k² · ĝ(t) ]
 *             / [ 1 + Δt · κ · k⁴ ]
 *
 * where κ = 1 (gradient energy coefficient) and mobility M = 1.
 *
 * Input file (input.dat) — one key-value pair per line:
 *   fluctuation  <value>   initial composition noise amplitude
 *   cAvg         <value>   mean composition
 *   lx           <int>     grid points in x
 *   ly           <int>     grid points in y
 *   mobility     <value>   (read but not used; kept for format compatibility)
 *   kappa        <value>   (read but not used; kept for format compatibility)
 *   delT         <value>   time step Δt
 *   delX         <value>   grid spacing in x
 *   delY         <value>   grid spacing in y
 *   timeInterval <value>   output interval
 *   totalTime    <value>   end time
 *   resume       <0|1>     0 = fresh start, 1 = resume
 *   resumeFrom   <value>   time to resume from (as a string to match filename)
 */

#include "ch_common.h"

/* ── Input parameters ─────────────────────────────────────────────────────── */
typedef struct {
    double fluctuation;   /* amplitude of initial random noise         */
    double c_avg;         /* mean composition                          */
    int    grid_x;        /* grid points in x                          */
    int    grid_y;        /* grid points in y                          */
    double mobility;      /* read for format compat. (unused here)     */
    double kappa;         /* gradient energy coefficient (unused here) */
    double dt;            /* time step                                 */
    double dx;            /* grid spacing in x                         */
    double dy;            /* grid spacing in y                         */
    double save_interval; /* output interval                           */
    double total_time;    /* total simulation time                     */
    int    resume;        /* 0 = fresh start, 1 = resume               */
    char   resume_from_str[32]; /* resume time as string (for filename) */
    double resume_from;   /* resume time as double                     */
} SimParams;

/* ── Read input.dat ───────────────────────────────────────────────────────── */
static void read_params(SimParams *p)
{
    /* kv_load parses the whole file; each parameter is looked up by name so
     * the order of lines in input.dat does not matter. */
    KVDoc doc         = kv_load("input.dat");
    p->fluctuation    = kv_get_double(&doc, "fluctuation");
    p->c_avg          = kv_get_double(&doc, "cAvg");
    p->grid_x         = kv_get_int   (&doc, "lx");
    p->grid_y         = kv_get_int   (&doc, "ly");
    p->mobility       = kv_get_double(&doc, "mobility");
    p->kappa          = kv_get_double(&doc, "kappa");
    p->dt             = kv_get_double(&doc, "delT");
    p->dx             = kv_get_double(&doc, "delX");
    p->dy             = kv_get_double(&doc, "delY");
    p->save_interval  = kv_get_double(&doc, "timeInterval");
    p->total_time     = kv_get_double(&doc, "totalTime");
    p->resume         = kv_get_int   (&doc, "resume");
    kv_get_string(&doc, "resumeFrom", p->resume_from_str, sizeof(p->resume_from_str));
    sscanf(p->resume_from_str, "%lf", &p->resume_from);
}

/* ── Free energy derivative  df/dc = -2c(1 + 2c² - 3c) ─────────────────── */
static inline double free_energy_deriv(double c)
{
    return -2.0 * c * (1.0 + 2.0 * c * c - 3.0 * c);
}

/* ── Main ─────────────────────────────────────────────────────────────────── */
int main(void)
{
    SimParams p;
    read_params(&p);

    int lx = p.grid_x;
    int ly = p.grid_y;
    int n_total = lx * ly;

    /* Allocate fields in Fourier-space representation */
    fftw_complex *composition       = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *composition_hat   = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *chem_potential    = fftw_malloc(sizeof(fftw_complex) * n_total);
    fftw_complex *chem_potential_hat= fftw_malloc(sizeof(fftw_complex) * n_total);

    if (!composition || !composition_hat || !chem_potential || !chem_potential_hat) {
        fprintf(stderr, "ERROR: FFTW allocation failed\n");
        return EXIT_FAILURE;
    }

    /* FFT plans:
     *   plan_fwd_c  : composition   → composition_hat   (forward)
     *   plan_fwd_mu : chem_potential → chem_potential_hat (forward)
     *   plan_bwd    : composition_hat → composition      (backward / IFFT)
     */
    fftw_plan plan_fwd_c   = fftw_plan_dft_2d(lx, ly, composition,    composition_hat,    FFTW_FORWARD,  FFTW_ESTIMATE);
    fftw_plan plan_fwd_mu  = fftw_plan_dft_2d(lx, ly, chem_potential,  chem_potential_hat, FFTW_FORWARD,  FFTW_ESTIMATE);
    fftw_plan plan_bwd     = fftw_plan_dft_2d(lx, ly, composition_hat, composition,        FFTW_BACKWARD, FFTW_ESTIMATE);

    /* Initialise composition field */
    if (p.resume == 0) {
        /* Fresh start: uniform c_avg plus small random fluctuation */
        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++)
                composition[IDX2(i, j, ly)] =
                    p.c_avg + (-1.0 + 2.0 * ((double)rand() / (double)RAND_MAX))
                              * (p.fluctuation * 10.0);
    } else {
        /* Resume: load previously saved field */
        char resume_path[80];
        snprintf(resume_path, sizeof(resume_path),
                 "Output/Data/output_%s.dat", p.resume_from_str);
        load_field_2d(composition, lx, ly, resume_path);
    }

    /* ── Time integration ─────────────────────────────────────────────────── */
    int step_start = (int)round(p.resume_from / p.dt);
    int step_end   = (int)round(p.total_time  / p.dt);

    for (int step = step_start; step <= step_end; step++) {
        double time = step * p.dt;

        /* Save field at requested output interval */
        if (should_save(step, p.dt, p.save_interval))
            save_field_2d(composition, lx, ly, time);

        /* Compute df/dc at every grid point */
        for (int i = 0; i < lx; i++)
            for (int j = 0; j < ly; j++)
                chem_potential[IDX2(i, j, ly)] =
                    free_energy_deriv(creal(composition[IDX2(i, j, ly)]));

        /* Forward FFT of composition and chemical potential */
        fftw_execute(plan_fwd_mu);
        fftw_execute(plan_fwd_c);

        /*
         * Semi-implicit spectral update in Fourier space:
         *   ĉ(t+Δt) = [ ĉ(t) + Δt·k²·μ̂(t) ] / [ 1 + Δt·k⁴ ]
         *
         * The k⁴ term in the denominator is the linearised stabiliser from
         * the gradient energy κ∇²c contribution (κ=1 here).
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

                composition_hat[idx] =
                    (composition_hat[idx] + p.dt * k2 * chem_potential_hat[idx])
                    / (1.0 + p.dt * k4);
            }
        }

        /* Inverse FFT back to real space */
        fftw_execute(plan_bwd);

        /* Normalise (FFTW does not normalise the inverse transform) */
        double norm = 1.0 / (double)n_total;
        for (int i = 0; i < n_total; i++)
            composition[i] *= norm;
    }

    /* ── Cleanup ──────────────────────────────────────────────────────────── */
    fftw_destroy_plan(plan_fwd_c);
    fftw_destroy_plan(plan_fwd_mu);
    fftw_destroy_plan(plan_bwd);
    fftw_free(composition);
    fftw_free(composition_hat);
    fftw_free(chem_potential);
    fftw_free(chem_potential_hat);
    fftw_cleanup();

    return EXIT_SUCCESS;
}
