/*
 * ch_common.h — shared utilities for all Cahn-Hilliard / post-processing solvers.
 *
 * Provides:
 *   - Unified includes
 *   - IDX2 / IDX3  – row-major flat-index macros
 *   - kfreq()      – shifted wavenumber for FFT mode i
 *   - fopen_or_die – checked file open
 *   - should_save  – integer step test (avoids fmod float-equality pitfalls)
 *   - KVDoc        – order-independent key-value parser for input.dat
 *   - save_field_2d / save_field_3d – composition output helpers
 *   - load_field_2d / load_field_3d – composition resume helpers
 */

#ifndef CH_COMMON_H
#define CH_COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <complex.h>
#include <fftw3.h>
#include "kv_parser.h"

#define CH_PI 3.14159265358979323846

/* ── Flat-index macros ────────────────────────────────────────────────────── */
/* Row-major 2-D:  element (i, j)    in an  lx × ly  grid */
#define IDX2(i, j, ly)           ((i)*(ly) + (j))
/* Row-major 3-D:  element (i, j, k) in an  lx × ly × lz  grid */
#define IDX3(i, j, k, ly, lz)   ((i)*(ly)*(lz) + (j)*(lz) + (k))

/* ── Wavenumber helper ────────────────────────────────────────────────────── */
/*
 * Returns the physical wavenumber for FFT mode i in a dimension of length n
 * with real-space grid spacing dx.
 * Implements the standard centred-frequency shift:
 *   modes 0 … n/2-1  → positive frequencies
 *   modes n/2 … n-1  → negative frequencies
 */
static inline double kfreq(int i, int n, double dx)
{
    double dk = 2.0 * CH_PI / ((double)n * dx);
    return (i < n / 2) ? (double)i * dk : (double)(i - n) * dk;
}

/* ── File helpers ─────────────────────────────────────────────────────────── */
static inline FILE *fopen_or_die(const char *path, const char *mode)
{
    FILE *f = fopen(path, mode);
    if (!f) {
        fprintf(stderr, "ERROR: cannot open '%s'\n", path);
        exit(EXIT_FAILURE);
    }
    return f;
}

/*
 * Integer step test: returns 1 when step n is an output step.
 * Integer modulo avoids floating-point equality issues with fmod.
 */
static inline int should_save(int n, double delt, double interval)
{
    long steps_per = (long)round(interval / delt);
    return steps_per > 0 && (n % steps_per == 0);
}

/* ── Field I/O ────────────────────────────────────────────────────────────── */

/* Write a 2-D composition field to Output/Data/output_<time>.dat */
static inline void save_field_2d(const fftw_complex *c, int lx, int ly, double time)
{
    char path[80];
    snprintf(path, sizeof(path), "Output/Data/output_%.2f.dat", time);
    FILE *f = fopen_or_die(path, "w");
    for (int i = 0; i < lx; i++) {
        for (int j = 0; j < ly; j++)
            fprintf(f, "%lf ", creal(c[IDX2(i, j, ly)]));
        fprintf(f, "\n");
    }
    fclose(f);
}

/* Write a 3-D composition field to Output/Data/output_<time>.dat */
static inline void save_field_3d(const fftw_complex *c, int lx, int ly, int lz,
                                   double time)
{
    char path[80];
    snprintf(path, sizeof(path), "Output/Data/output_%.2f.dat", time);
    FILE *f = fopen_or_die(path, "w");
    for (int i = 0; i < lx; i++)
        for (int j = 0; j < ly; j++)
            for (int k = 0; k < lz; k++)
                fprintf(f, "%le\n", creal(c[IDX3(i, j, k, ly, lz)]));
    fclose(f);
}

/* Load a 2-D composition field saved by save_field_2d */
static inline void load_field_2d(fftw_complex *c, int lx, int ly, const char *path)
{
    FILE *f = fopen_or_die(path, "r");
    for (int i = 0; i < lx; i++)
        for (int j = 0; j < ly; j++) {
            double val;
            if (fscanf(f, "%lf", &val) != 1) {
                fprintf(stderr, "ERROR: unexpected EOF reading '%s'\n", path);
                fclose(f);
                exit(EXIT_FAILURE);
            }
            c[IDX2(i, j, ly)] = val;
        }
    fclose(f);
}

/* Load a 3-D composition field saved by save_field_3d */
static inline void load_field_3d(fftw_complex *c, int lx, int ly, int lz,
                                   const char *path)
{
    FILE *f = fopen_or_die(path, "r");
    for (int i = 0; i < lx; i++)
        for (int j = 0; j < ly; j++)
            for (int k = 0; k < lz; k++) {
                double val;
                if (fscanf(f, "%le", &val) != 1) {
                    fprintf(stderr, "ERROR: unexpected EOF reading '%s'\n", path);
                    fclose(f);
                    exit(EXIT_FAILURE);
                }
                c[IDX3(i, j, k, ly, lz)] = val;
            }
    fclose(f);
}

#endif /* CH_COMMON_H */
