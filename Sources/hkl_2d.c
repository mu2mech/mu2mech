/*
 * hkl_2d.c — 2-D particle labelling and size analysis.
 *
 * Reads a composition field from Output/Data/output_<time>.dat and:
 *   1. Labels connected regions where composition > PHASE_THRESHOLD (0.5).
 *   2. Computes the volume (pixel count) of each particle.
 *   3. Estimates an effective radius from  r = sqrt(V/π).
 *   4. Writes per-particle data to Output/PostData/volume_<time>.dat.
 *   5. Appends average-radius summary to Output/PostData/avg_rad_<time>.dat.
 *
 * Labelling uses a two-pass connected-component algorithm with periodic
 * boundary conditions.
 *
 * Input file (input.dat):
 *   lx    <int>    grid points in x
 *   ly    <int>    grid points in y
 *   time  <float>  snapshot time (used to build the filename)
 */

#include "kv_parser.h"   /* KVDoc, kv_load, kv_get_* — no FFTW dependency */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define PHASE_THRESHOLD  0.5   /* composition threshold that defines a particle */
#define MAX_PARTICLES   200000 /* upper bound on number of distinct particles    */

/* ── Forward declarations ─────────────────────────────────────────────────── */
static int min_nonzero_label(int left, int down, int right, int up);

/* ── File helper ──────────────────────────────────────────────────────────── */
static FILE *fopen_or_die(const char *path, const char *mode)
{
    FILE *f = fopen(path, mode);
    if (!f) {
        fprintf(stderr, "ERROR: cannot open '%s'\n", path);
        exit(EXIT_FAILURE);
    }
    return f;
}

/* ── Flat index for a 2-D grid of width ny ───────────────────────────────── */
#define IDX(i, j, ny) ((i)*(ny) + (j))

/* ── Main ─────────────────────────────────────────────────────────────────── */
int main(void)
{
    /* Read grid dimensions and snapshot time from input.dat */
    int   grid_x, grid_y;
    float snapshot_time;
    {
        KVDoc doc    = kv_load("input.dat");
        grid_x       = kv_get_int   (&doc, "lx");
        grid_y       = kv_get_int   (&doc, "ly");
        snapshot_time= (float)kv_get_double(&doc, "time");
    }

    /* Allocate composition and particle-label arrays */
    double *composition = (double *)malloc((size_t)grid_x * grid_y * sizeof(double));
    int    *label       = (int    *)malloc((size_t)grid_x * grid_y * sizeof(int));
    if (!composition || !label) {
        fprintf(stderr, "ERROR: allocation failed\n");
        return EXIT_FAILURE;
    }

    /* Read composition field */
    char input_path[80];
    snprintf(input_path, sizeof(input_path),
             "./Output/Data/output_%0.2f.dat", snapshot_time);
    FILE *fp_field = fopen_or_die(input_path, "r");
    for (int i = 0; i < grid_x; i++) {
        for (int j = 0; j < grid_y; j++) {
            label[IDX(i, j, grid_y)] = 0;
            fscanf(fp_field, "%lf ", &composition[IDX(i, j, grid_y)]);
        }
        fscanf(fp_field, "\n");
    }
    fclose(fp_field);

    /* ── First pass: assign initial labels ────────────────────────────────── */
    int next_label = 1;   /* next unused particle label */
    for (int i = 0; i < grid_x; i++) {
        for (int j = 0; j < grid_y; j++) {
            int ijk = IDX(i, j, grid_y);

            if (composition[ijk] <= PHASE_THRESHOLD || label[ijk] != 0)
                continue;

            /* Periodic neighbour indices */
            int i_plus  = (i + 1) % grid_x;
            int i_minus = (i - 1 + grid_x) % grid_x;
            int j_plus  = (j + 1) % grid_y;
            int j_minus = (j - 1 + grid_y) % grid_y;

            int lbl_left  = label[IDX(i_minus, j,       grid_y)];
            int lbl_right = label[IDX(i_plus,  j,       grid_y)];
            int lbl_down  = label[IDX(i,       j_minus, grid_y)];
            int lbl_up    = label[IDX(i,       j_plus,  grid_y)];

            if (lbl_left || lbl_right || lbl_down || lbl_up)
                label[ijk] = min_nonzero_label(lbl_left, lbl_down, lbl_right, lbl_up);
            else
                label[ijk] = next_label++;
        }
    }

    /* ── Second pass: merge conflicting labels ────────────────────────────── */
    for (int i = 0; i < grid_x; i++) {
        for (int j = 0; j < grid_y; j++) {
            int ijk = IDX(i, j, grid_y);
            if (label[ijk] == 0) continue;

            int i_plus  = (i + 1) % grid_x;
            int i_minus = (i - 1 + grid_x) % grid_x;
            int j_plus  = (j + 1) % grid_y;
            int j_minus = (j - 1 + grid_y) % grid_y;

            int lbl_left  = label[IDX(i_minus, j,       grid_y)];
            int lbl_right = label[IDX(i_plus,  j,       grid_y)];
            int lbl_down  = label[IDX(i,       j_minus, grid_y)];
            int lbl_up    = label[IDX(i,       j_plus,  grid_y)];

            if (!(lbl_left || lbl_right || lbl_down || lbl_up)) continue;

            int min_lbl = min_nonzero_label(lbl_left, lbl_down, lbl_right, lbl_up);
            int cur_lbl = label[ijk];

            if (cur_lbl > min_lbl) {
                /* Relabel all pixels with cur_lbl to min_lbl */
                for (int a = 0; a < grid_x; a++)
                    for (int b = 0; b < grid_y; b++)
                        if (label[IDX(a, b, grid_y)] == cur_lbl)
                            label[IDX(a, b, grid_y)] = min_lbl;
            }
        }
    }

    /* ── Compute particle volumes ─────────────────────────────────────────── */
    int *volume = (int *)calloc(next_label, sizeof(int));
    if (!volume) { fprintf(stderr, "ERROR: volume allocation failed\n"); return EXIT_FAILURE; }

    for (int i = 0; i < grid_x; i++)
        for (int j = 0; j < grid_y; j++) {
            int lbl = label[IDX(i, j, grid_y)];
            if (lbl > 0 && lbl < next_label)
                volume[lbl]++;
        }

    /* ── Write per-particle output ────────────────────────────────────────── */
    char volume_path[80];
    snprintf(volume_path, sizeof(volume_path),
             "./Output/PostData/volume_%0.2f.dat", snapshot_time);
    FILE *fp_vol = fopen_or_die(volume_path, "w");

    double *radius    = (double *)calloc(next_label, sizeof(double));
    double  r_avg     = 0.0;
    int     n_particles = 0;

    for (int a = 1; a < next_label; a++) {
        if (volume[a] <= 0) continue;
        n_particles++;
        /* 2-D: r = sqrt(V/π)  — effective circle radius */
        radius[a] = sqrt((double)volume[a] / M_PI);
        r_avg    += radius[a];
        fprintf(fp_vol, "%d %d %d %lf\n", n_particles, a, volume[a], radius[a]);
    }
    fclose(fp_vol);

    r_avg = (n_particles > 0) ? r_avg / (double)n_particles : 0.0;

    /* ── Append summary statistics ────────────────────────────────────────── */
    char avg_path[80];
    snprintf(avg_path, sizeof(avg_path),
             "./Output/PostData/avg_rad_%0.2f.dat", snapshot_time);
    FILE *fp_avg = fopen_or_die(avg_path, "a");
    /* columns: time, r_avg, r_avg^4 (Lifshitz-Slyozov diagnostic), n_particles */
    fprintf(fp_avg, "%lf %lf %lf %d\n",
            (double)snapshot_time,
            r_avg,
            r_avg * r_avg * r_avg * r_avg,
            n_particles);
    fclose(fp_avg);

    /* ── Cleanup ──────────────────────────────────────────────────────────── */
    free(composition);
    free(label);
    free(volume);
    free(radius);

    return EXIT_SUCCESS;
}

/* ── min_nonzero_label ────────────────────────────────────────────────────── *
 * Returns the smallest positive label among the four neighbours.
 * Zero-valued neighbours (unlabelled) are ignored.
 */
static int min_nonzero_label(int left, int down, int right, int up)
{
    int candidates[4] = { left, down, right, up };

    /* Bubble-sort the four values */
    for (int i = 0; i < 4; i++)
        for (int j = i + 1; j < 4; j++)
            if (candidates[i] > candidates[j]) {
                int tmp = candidates[i];
                candidates[i] = candidates[j];
                candidates[j] = tmp;
            }

    /* Return the first positive candidate */
    for (int i = 0; i < 4; i++)
        if (candidates[i] > 0)
            return candidates[i];

    return 0; /* all neighbours are unlabelled */
}
