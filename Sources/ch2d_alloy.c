#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <fftw3.h>
#include <time.h>
#include <math.h>
#include "nrutil.c"
#include "gasdev.c"
#define pi 3.14159265

/* Evolution of microstructure of composition in spinoidal range */
/* Order of fluctuation or noise added */
/* Flag is added */

int main()
{

   /* Data initialization */

   int lx, ly, k, x, y, n, N, i, j, ij, resume, total_time_steps;
   double delt, delkx, delky, halflx, halfly, kfx, kfy, kfx2, kfy2, k2, k4, delx, dely, c_avg;
   char junk[100];
   char resume_from_str[10];
   double resume_from;
   double time, time_interval, total_time;
   double fluctuation;
   double aa, bb, cc, dd, ee, pp1, pp2;

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
   %s%lf\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%d\
   %s%d\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%d\
   %s%s",
          junk, &aa,
          junk, &bb,
          junk, &cc,
          junk, &dd,
          junk, &ee,
          junk, &fluctuation,
          junk, &c_avg,
          junk, &lx,
          junk, &ly,
          junk, &delt,
          junk, &delx,
          junk, &dely,
          junk, &time_interval,
          junk, &total_time,
          junk, &resume,
          junk, &resume_from_str);

   fclose(fp);

   sscanf(resume_from_str, "%lf", &resume_from);

   /* Defining variables in fourier space */

   fftw_complex *c, *ctilda, *g, *gtilda, *mobility;

   c = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   ctilda = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   g = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   gtilda = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   mobility = fftw_malloc(sizeof(fftw_complex) * lx * ly);

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

      /* Loading initial composition */

      FILE *fp;
      char fName[30] = "";
      strcat(fName, "Output/Data/output_");
      strcat(fName, resume_from_str);
      strcat(fName, ".dat");
      fp = fopen(fName, "r");
      if (fp == NULL)
      {
         printf("Cannot open file\n");
         return 1;
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

   /* Defining initial composition */

   double **random_numA, **random_numB, **random_numC, **random_numD;
   float gasdev(long *idum);
   double rsum1, rmean1, rsum2, rmean2, rsum3, rmean3, rsum4, rmean4;

   pp1 = (-6 * bb + sqrt(36 * bb * bb - 96 * aa * cc)) / (24 * aa);
   pp2 = (-6 * bb - sqrt(36 * bb * bb - 96 * aa * cc)) / (24 * aa);

   if ((c_avg >= pp1) || (c_avg <= pp2))
   {

      long int SEED = -94929;
      long int SEED2 = -81659;
      long int SEED3 = -15816;
      long int SEED4 = -49369;

      random_numA = dmatrix(0, lx, 0, ly);
      random_numB = dmatrix(0, lx, 0, ly);
      random_numC = dmatrix(0, lx, 0, ly);
      random_numD = dmatrix(0, lx, 0, ly);

      for (i = 0; i < lx; ++i)
      {
         for (j = 0; j < ly; ++j)
         {
            ij = i * ly + j;

            random_numA[i][j] = 0.0;
            random_numB[i][j] = 0.0;
            random_numC[i][j] = 0.0;
            random_numD[i][j] = 0.0;
         }
      }

      for (i = 0; i < lx; ++i)
      {
         for (j = 0; j < ly; ++j)
         {
            ij = i * ly + j;

            random_numA[i][j] = gasdev(&SEED);
            random_numB[i][j] = gasdev(&SEED2);
            random_numC[i][j] = gasdev(&SEED3);
            random_numD[i][j] = gasdev(&SEED4);
         }
      }

      rsum1 = 0.0;
      rsum2 = 0.0;
      rsum3 = 0.0;
      rsum4 = 0.0;

      for (i = 0; i < lx; ++i)
      {
         for (j = 0; j < ly; ++j)
         {
            ij = i * ly + j;

            random_numA[i][j] = random_numA[i][j] * 0.005;
            rsum1 += random_numA[i][j];
            random_numB[i][j] = random_numB[i][j] * 0.005;
            rsum2 += random_numB[i][j];
            random_numC[i][j] = random_numC[i][j] * 0.005;
            rsum3 += random_numC[i][j];
            random_numD[i][j] = random_numD[i][j] * 0.005;
            rsum4 += random_numD[i][j];
         }
      }
      rmean1 = rsum1 / (double)(lx * ly);
      rmean2 = rsum2 / (double)(lx * ly);
      rmean3 = rsum3 / (double)(lx * ly);
      rmean4 = rsum4 / (double)(lx * ly);

      for (i = 0; i < lx; ++i)
      {
         for (j = 0; j < ly; ++j)
         {
            ij = i * ly + j;

            c[ij] += random_numA[i][j] - rmean1;
            c[ij] += random_numB[i][j] - rmean2;
            c[ij] += random_numC[i][j] - rmean3;
            c[ij] += random_numD[i][j] - rmean4;
         }
      }

      free_dmatrix(random_numA, 0, lx, 0, ly);
      free_dmatrix(random_numB, 0, lx, 0, ly);
      free_dmatrix(random_numC, 0, lx, 0, ly);
      free_dmatrix(random_numD, 0, lx, 0, ly);

      delkx = 2.0 * pi / (lx * delx);
      delky = 2.0 * pi / (ly * dely);

      halflx = (int)lx / 2.0;
      halfly = (int)ly / 2.0;

      /* Running the code for given time */

      total_time_steps = ((total_time) / delt);

      for (n = 1; n <= total_time_steps; ++n)

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
         }

         /* Defining free energy */

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)
            {

               g[y + ly * x] = -(4 * aa * (c[y + ly * x]) * (c[y + ly * x]) * (c[y + ly * x]) + 3 * bb * (c[y + ly * x]) * (c[y + ly * x]) + 2 * cc * (c[y + ly * x]) + dd); /* Derivative of  free energy */
                                                                                                                                                                             // mobility[y+ly*x] = fabs(1/(12*aa*(c[y+ly*x])*(c[y+ly*x]) + 6*bb*(c[y+ly*x])+ 2*cc));
               mobility[y + ly * x] = (c[y + ly * x]) * (1 - c[y + ly * x]);
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

               ctilda[j + ly * i] = 1. * (ctilda[j + ly * i] + 2 * delt * mobility[j + ly * i] * k2 * gtilda[j + ly * i]) / (1.0 + 2 * delt * mobility[j + ly * i] * k4); /* no need need to define new variable and replace ctilda values */
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

         /* Noise generation upto 1000 time steps */

         if (n <= 1000)
         {
            long int SEED = -949;
            long int SEED2 = -819;
            long int SEED3 = -16;
            long int SEED4 = -49;

            random_numA = dmatrix(0, lx, 0, ly);
            random_numB = dmatrix(0, lx, 0, ly);
            random_numC = dmatrix(0, lx, 0, ly);
            random_numD = dmatrix(0, lx, 0, ly);

            for (i = 0; i < lx; ++i)
            {
               for (j = 0; j < ly; ++j)
               {
                  ij = i * ly + j;

                  random_numA[i][j] = 0.0;
                  random_numB[i][j] = 0.0;
                  random_numC[i][j] = 0.0;
                  random_numD[i][j] = 0.0;
               }
            }

            for (i = 0; i < lx; ++i)
            {
               for (j = 0; j < ly; ++j)
               {
                  ij = i * ly + j;

                  random_numA[i][j] = gasdev(&SEED);
                  random_numB[i][j] = gasdev(&SEED2);
                  random_numC[i][j] = gasdev(&SEED3);
                  random_numD[i][j] = gasdev(&SEED4);
               }
            }

            rsum1 = 0.0;
            rsum2 = 0.0;
            rsum3 = 0.0;
            rsum4 = 0.0;

            for (i = 0; i < lx; ++i)
            {
               for (j = 0; j < ly; ++j)
               {
                  ij = i * ly + j;

                  random_numA[i][j] = random_numA[i][j] * 0.005;
                  rsum1 += random_numA[i][j];
                  random_numB[i][j] = random_numB[i][j] * 0.005;
                  rsum2 += random_numB[i][j];
                  random_numC[i][j] = random_numC[i][j] * 0.005;
                  rsum3 += random_numC[i][j];
                  random_numD[i][j] = random_numD[i][j] * 0.005;
                  rsum4 += random_numD[i][j];
               }
            }
            rmean1 = rsum1 / (double)(lx * ly);
            rmean2 = rsum2 / (double)(lx * ly);
            rmean3 = rsum3 / (double)(lx * ly);
            rmean4 = rsum4 / (double)(lx * ly);

            for (i = 0; i < lx; ++i)
            {
               for (j = 0; j < ly; ++j)
               {
                  ij = i * ly + j;

                  c[ij] += random_numA[i][j] - rmean1;
                  c[ij] += random_numB[i][j] - rmean2;
                  c[ij] += random_numC[i][j] - rmean3;
                  c[ij] += random_numD[i][j] - rmean4;
               }
            }

            free_dmatrix(random_numA, 0, lx, 0, ly);
            free_dmatrix(random_numB, 0, lx, 0, ly);
            free_dmatrix(random_numC, 0, lx, 0, ly);
            free_dmatrix(random_numD, 0, lx, 0, ly);
         }
      }
   }

   if ((c_avg <= pp1) && (c_avg >= pp2))
   {

      for (x = 0; x < lx; ++x)
      {
         for (y = 0; y < ly; ++y)
         {

            {
               c[y + ly * x] = c_avg + (-1 + 2 * ((double)rand() / (double)RAND_MAX)) / 200; /* ((double)rand()/(double)RAND_MAX) generates the random no. between 0 and 1*/
            }
         }
      }

      delkx = 2.0 * pi / (lx * delx);
      delky = 2.0 * pi / (ly * dely);

      halflx = (int)lx / 2.0;
      halfly = (int)ly / 2.0;

      /* Running the code for given time */

      total_time_steps = ((total_time) / delt);

      for (n = 1; n <= total_time_steps; ++n)
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
         }

         /* Defining free energy */

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)
            {

               g[y + ly * x] = -(4 * aa * (c[y + ly * x]) * (c[y + ly * x]) * (c[y + ly * x]) + 3 * bb * (c[y + ly * x]) * (c[y + ly * x]) + 2 * cc * (c[y + ly * x]) + dd); /* Derivative of  free energy */
                                                                                                                                                                             // mobility[y+ly*x] = fabs(1/(12*aa*(c[y+ly*x])*(c[y+ly*x]) + 6*bb*(c[y+ly*x])+ 2*cc));
               mobility[y + ly * x] = (c[y + ly * x]) * (1 - c[y + ly * x]);
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

               ctilda[j + ly * i] = 1. * (ctilda[j + ly * i] + 2 * delt * mobility[j + ly * i] * k2 * gtilda[j + ly * i]) / (1.0 + 2 * delt * mobility[j + ly * i] * k4); /* no need need to define new variable and replace ctilda values */
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
   }

   fftw_free(c);
   fftw_free(g);
   fftw_free(mobility);

   fftw_destroy_plan(p);
   fftw_destroy_plan(q);
   fftw_destroy_plan(s);

   fftw_cleanup();

   return 0;
}
