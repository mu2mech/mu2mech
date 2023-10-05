#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <fftw3.h>
#include <time.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define pi 3.14159265

     /* Evolution of microstructure of composition in spinoidal range */

int main()
{
    /* Data initialization */

    int    lx, ly, M, k, x, y, n, N, i, j, resume, total_time_steps;
    double delt, delkx, delky, halflx, halfly, kfx, kfy, kfx2, kfy2, k2, k4, delx, dely, c_avg;
    char   junk[100];
    char   resume_from_str[10];
    double resume_from;
    double time, time_interval, total_time;
    double fluctuation;

    /* Creating a file and Getting data from input file */

    FILE *fp;
    fp = fopen("Sources/input.dat", "r"); 

    if (fp == NULL)
    {
        printf("Cannot open file");
    }
    fscanf(fp, "\
   %s%lf\
   %s%lf\
   %s%d\
   %s%d\
   %s%d\
   %s%lf\
   %s%d\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%d\
   %s%s",
           junk, &fluctuation,
           junk, &c_avg,
           junk, &lx,
           junk, &ly,
           junk, &M,
           junk, &delt,
           junk, &k,
           junk, &delx,
           junk, &dely,
           junk, &time_interval,
           junk, &total_time,
           junk, &resume,
           junk, &resume_from_str);

    fclose(fp);

    sscanf(resume_from_str, "%lf", &resume_from);

    /* Defining variables in fourier space */

    fftw_complex *c, *ctilda, *g, *gtilda;

    c      = fftw_malloc(sizeof(fftw_complex) * lx * ly);
    ctilda = fftw_malloc(sizeof(fftw_complex) * lx * ly);
    g      = fftw_malloc(sizeof(fftw_complex) * lx * ly);
    gtilda = fftw_malloc(sizeof(fftw_complex) * lx * ly);

    /* Defining FFT Plans */

    fftw_plan p, q, s;

    p = fftw_plan_dft_2d(lx, ly, c, ctilda, FFTW_FORWARD, FFTW_ESTIMATE);
    q = fftw_plan_dft_2d(lx, ly, g, gtilda, FFTW_FORWARD, FFTW_ESTIMATE);
    s = fftw_plan_dft_2d(lx, ly, ctilda, c, FFTW_BACKWARD, FFTW_ESTIMATE);

    // resume = 0 - Start calculation from the beginning
    // resume = 1 - Resume calculation

    if (resume == 0)
    {
        /* Defining initial composition */
        /* Providing noise from -0.001 to +0.001*/

        for (x = 0; x < lx; ++x)
        {
            for (y = 0; y < ly; ++y)
            {
                c[y + ly * x] = c_avg + (-1 + 2 * ((double)rand() / (double)RAND_MAX)) * (fluctuation * 10);
            }
        }
    }

    else
    {
        // Loading initial composition

        FILE *fp;
        char fName[30];
        strcat(fName, "Output/Data/output_");
        strcat(fName, resume_from_str);
        strcat(fName, ".dat");
        fp = fopen(fName, "r");
        if (fp == NULL)
        {
            printf("Cannot open file");
        }
        for (x = 0; x < lx; ++x)
        {
            for (y = 0; y < ly; ++y)
            {

                fscanf(fp, "%lf", &c[y + ly * x]);
            }
            fscanf(fp, "%lf", &c[y + ly * x]);
        }
    }

    delkx = 2.0 * pi / (lx * delx);
    delky = 2.0 * pi / (ly * dely);

    halflx = (int)lx / 2.0;
    halfly = (int)ly / 2.0;

    /* Running the code for given time */

    total_time_steps = ((total_time) / delt);
    n = ((resume_from) / delt);

    for (; n <= total_time_steps; ++n)
    {

    /* Saving data to files */       

        time = n * delt;
        if (fmod(time, time_interval) == 0)
        {
            char file_name[25];
            sprintf(file_name, "Output/Data/output_%.2f.dat", time);
            FILE *fptr;
            fptr = fopen(file_name, "w");

            for (x = 0; x < lx; ++x)
            {
                for (y = 0; y < ly; ++y)
                {
                    fprintf(fptr, "%f ", creal(c[y + ly * x]));
                }
                fprintf(fptr, "%f\n", creal(c[y + ly * x]));
            }
            fclose(fptr);
            // printf("output_%.2f.dat\n", time);
        }

        /* Defining free energy */

        for (x = 0; x < lx; ++x)
        {
            for (y = 0; y < ly; ++y)
            {

                g[y + ly * x] = -2 * (c[y + ly * x]) * (1 + 2 * (c[y + ly * x]) * (c[y + ly * x]) - 3 * (c[y + ly * x]));
            }
        }

        /* FFT of composition and  free energy */

        fftw_execute(q);
        fftw_execute(p);

        for (i = 0; i < lx; ++i)
        {
            if (i < halflx)
            {
                kfx = i * delkx;
            }

            else
            {
                kfx = (i - lx) * delkx;
            }
            kfx2 = kfx * kfx;

            for (j = 0; j < ly; ++j)
            {
                if (j < halfly)
                {
                    kfy = j * delky;
                }

                else
                {
                    kfy = (j - ly) * delky;
                }

                kfy2 = kfy * kfy;
                k2 = kfx2 + kfy2;
                k4 = k2 * k2;

                ctilda[j + ly * i] = 1. * (ctilda[j + ly * i] + delt * k2 * gtilda[j + ly * i]) / (1.0 + delt * k4); 
            }
        }

        /* IFFT of final composition */

        fftw_execute(s);

        /* Normalization of composition */

        for (x = 0; x < lx; ++x)
        {
            for (y = 0; y < ly; ++y)
            {
                c[y + ly * x] = 1. * c[y + ly * x] / (lx * ly); 
            }
        }
    }

    fftw_free(c);
    fftw_free(g);

    fftw_destroy_plan(p);
    fftw_destroy_plan(q);
    fftw_destroy_plan(s);

    fftw_cleanup();
    printf("Program terminated");
    return 0;
}
