/*
 * hkl_3d.c — 3-D particle labelling and size analysis.
 *
 * Identical in structure to hkl_2d.c but operates on a 3-D composition field.
 * Reads Output/Data/output_<time>.dat written by ch3d_alloy (one value per line).
 *
 * Effective radius from  r = (3V / 4π)^(1/3).
 *
 * Input file (input.dat):
 *   lx    <int>    grid points in x
 *   ly    <int>    grid points in y
 *   lz    <int>    grid points in z
 *   time  <float>  snapshot time
 */

#include "kv_parser.h"   /* KVDoc, kv_load, kv_get_* — no FFTW dependency */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

#define PHASE_THRESHOLD  0.5
#define MAX_PARTICLES   200000

/* ── Forward declarations ─────────────────────────────────────────────────── */
static int min_nonzero_label_6(int left, int down, int back,
                                int right, int up,  int front);

/* ── File helper for data/output files (separate from kv_parser's helper) ── */
static FILE *fopen_or_die(const char *path, const char *mode)
{
    FILE *f = fopen(path, mode);
    if (!f) {
        fprintf(stderr, "ERROR: cannot open '%s'\n", path);
        exit(EXIT_FAILURE);
    }
    return f;
}

/* ── Flat index for (i, j, k) in an lx × ly × lz grid ───────────────────── */
#define IDX3(i, j, k, ny, nz) ((i)*(ny)*(nz) + (j)*(nz) + (k))

/* ── Main ─────────────────────────────────────────────────────────────────── */
int main(void)
{
    /* Read grid dimensions and snapshot time from input.dat */
    int   grid_x, grid_y, grid_z;
    float snapshot_time;
    {
        KVDoc doc     = kv_load("input.dat");
        grid_x        = kv_get_int   (&doc, "lx");
        grid_y        = kv_get_int   (&doc, "ly");
        grid_z        = kv_get_int   (&doc, "lz");
        snapshot_time = (float)kv_get_double(&doc, "time");
    }

    size_t n_total = (size_t)grid_x * grid_y * grid_z;

    /*
     * Allocate after reading dimensions so sizes are correct.
     * (Original code allocated with hardcoded defaults before reading the file.)
     */
    double *composition = (double *)malloc(n_total * sizeof(double));
    int    *label       = (int    *)malloc(n_total * sizeof(int));
    if (!composition || !label) {
        fprintf(stderr, "ERROR: allocation failed\n");
        return EXIT_FAILURE;
    }

    /* Read composition field.
     * ch3d_alloy writes one value per line ("%le\n") — match that format. */
    char input_path[80];
    snprintf(input_path, sizeof(input_path),
             "./Output/Data/output_%0.2f.dat", snapshot_time);
    FILE *fp_field = fopen_or_die(input_path, "r");
    for (size_t n = 0; n < n_total; n++) {
        label[n] = 0;
        if (fscanf(fp_field, "%lf", &composition[n]) != 1) {
            fprintf(stderr, "ERROR: unexpected EOF in '%s'\n", input_path);
            fclose(fp_field);
            return EXIT_FAILURE;
        }
    }
    fclose(fp_field);

    /* ── First pass: assign initial labels ────────────────────────────────── */
    int next_label = 1;
    for (int i = 0; i < grid_x; i++) {
        for (int j = 0; j < grid_y; j++) {
            for (int k = 0; k < grid_z; k++) {
                int ijk = IDX3(i, j, k, grid_y, grid_z);

                if (composition[ijk] <= PHASE_THRESHOLD || label[ijk] != 0)
                    continue;

                /* Periodic neighbour indices */
                int i_plus  = (i + 1) % grid_x;
                int i_minus = (i - 1 + grid_x) % grid_x;
                int j_plus  = (j + 1) % grid_y;
                int j_minus = (j - 1 + grid_y) % grid_y;
                int k_plus  = (k + 1) % grid_z;
                int k_minus = (k - 1 + grid_z) % grid_z;

                int lbl_left  = label[IDX3(i_minus, j,      k,      grid_y, grid_z)];
                int lbl_right = label[IDX3(i_plus,  j,      k,      grid_y, grid_z)];
                int lbl_down  = label[IDX3(i,       j_minus,k,      grid_y, grid_z)];
                int lbl_up    = label[IDX3(i,       j_plus, k,      grid_y, grid_z)];
                int lbl_back  = label[IDX3(i,       j,      k_minus,grid_y, grid_z)];
                int lbl_front = label[IDX3(i,       j,      k_plus, grid_y, grid_z)];

                if (lbl_left || lbl_right || lbl_down ||
                    lbl_up   || lbl_back  || lbl_front)
                    label[ijk] = min_nonzero_label_6(lbl_left,  lbl_down, lbl_back,
                                                     lbl_right, lbl_up,   lbl_front);
                else
                    label[ijk] = next_label++;
            }
        }
    }

    /* ── Second pass: merge conflicting labels ────────────────────────────── */
    for (int i = 0; i < grid_x; i++) {
        for (int j = 0; j < grid_y; j++) {
            for (int k = 0; k < grid_z; k++) {
                int ijk = IDX3(i, j, k, grid_y, grid_z);
                if (label[ijk] == 0) continue;

                int i_plus  = (i + 1) % grid_x;
                int i_minus = (i - 1 + grid_x) % grid_x;
                int j_plus  = (j + 1) % grid_y;
                int j_minus = (j - 1 + grid_y) % grid_y;
                int k_plus  = (k + 1) % grid_z;
                int k_minus = (k - 1 + grid_z) % grid_z;

                int lbl_left  = label[IDX3(i_minus, j,      k,      grid_y, grid_z)];
                int lbl_right = label[IDX3(i_plus,  j,      k,      grid_y, grid_z)];
                int lbl_down  = label[IDX3(i,       j_minus,k,      grid_y, grid_z)];
                int lbl_up    = label[IDX3(i,       j_plus, k,      grid_y, grid_z)];
                int lbl_back  = label[IDX3(i,       j,      k_minus,grid_y, grid_z)];
                int lbl_front = label[IDX3(i,       j,      k_plus, grid_y, grid_z)];

                if (!(lbl_left || lbl_right || lbl_down ||
                      lbl_up   || lbl_back  || lbl_front)) continue;

                int min_lbl = min_nonzero_label_6(lbl_left,  lbl_down, lbl_back,
                                                  lbl_right, lbl_up,   lbl_front);
                int cur_lbl = label[ijk];

                if (cur_lbl > min_lbl) {
                    for (size_t n = 0; n < n_total; n++)
                        if (label[n] == cur_lbl)
                            label[n] = min_lbl;
                }
            }
        }
    }

    /* ── Compute particle volumes ─────────────────────────────────────────── */
    int *volume = (int *)calloc(next_label, sizeof(int));
    if (!volume) { fprintf(stderr, "ERROR: volume allocation failed\n"); return EXIT_FAILURE; }

    for (size_t n = 0; n < n_total; n++) {
        int lbl = label[n];
        if (lbl > 0 && lbl < next_label)
            volume[lbl]++;
    }

    /* ── Write per-particle output ────────────────────────────────────────── */
    char volume_path[80];
    snprintf(volume_path, sizeof(volume_path),
             "./Output/PostData/volume_%0.2f.dat", snapshot_time);
    FILE *fp_vol = fopen_or_die(volume_path, "w");

    double *radius      = (double *)calloc(next_label, sizeof(double));
    double  r_avg       = 0.0;
    int     n_particles = 0;

    for (int a = 1; a < next_label; a++) {
        if (volume[a] <= 0) continue;
        n_particles++;
        /* 3-D: r = (3V / 4π)^(1/3) */
        radius[a] = pow(3.0 * volume[a] / (4.0 * M_PI), 1.0 / 3.0);
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
    fprintf(fp_avg, "%lf %lf %d\n",
            (double)snapshot_time, r_avg, n_particles);
    fclose(fp_avg);

    /* ── Cleanup ──────────────────────────────────────────────────────────── */
    free(composition);
    free(label);
    free(volume);
    free(radius);

    return EXIT_SUCCESS;
}

/* ── min_nonzero_label_6 ─────────────────────────────────────────────────── *
 * Returns the smallest positive label among the six face neighbours.
 */
static int min_nonzero_label_6(int left, int down, int back,
                                int right, int up,  int front)
{
    int c[6] = { left, down, back, right, up, front };

    /* Insertion sort (tiny array — no need for qsort overhead) */
    for (int i = 1; i < 6; i++) {
        int key = c[i], j = i - 1;
        while (j >= 0 && c[j] > key) { c[j + 1] = c[j]; j--; }
        c[j + 1] = key;
    }

    for (int i = 0; i < 6; i++)
        if (c[i] > 0)
            return c[i];

    return 0;
}
