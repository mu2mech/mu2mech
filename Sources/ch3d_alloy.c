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

int main()
{
   /* Data initialization */
   int lx, ly, lz, M, k, x, y, z, n, N, i, j, kk, ij, m, resume, total_time_steps;
   double delt, flag_time, delkx, delky, delkz, halflx, halfly, halflz, kfx, kfy, kfz, kfx2, kfy2, kfz2, k2, k4, delx, dely, delz, c_avg, fluctuation;
   char junk[100];
   char resume_from_str[10];
   double resume_from;
   double time, time_interval, total_time;
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
   %s%d\
   %s%d\
   %s%lf\
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
          junk, &lz,
          junk, &M,
          junk, &delt,
          junk, &k,
          junk, &delx,
          junk, &dely,
          junk, &delz,
          junk, &time_interval,
          junk, &total_time,
          junk, &resume,
          junk, &resume_from_str);

   fclose(fp);
   sscanf(resume_from_str, "%lf", &resume_from);

   /* Defining variables in fourier space */

   fftw_complex *c, *ctilda, *g, *gtilda;

   c      = fftw_malloc(sizeof(fftw_complex) * lx * ly * lz);
   ctilda = fftw_malloc(sizeof(fftw_complex) * lx * ly * lz);
   g      = fftw_malloc(sizeof(fftw_complex) * lx * ly * lz);
   gtilda = fftw_malloc(sizeof(fftw_complex) * lx * ly * lz);

   /* Defining FFT Plans */

   fftw_plan p, q, s;

   p = fftw_plan_dft_3d(lx, ly, lz, c, ctilda, FFTW_FORWARD, FFTW_ESTIMATE);
   q = fftw_plan_dft_3d(lx, ly, lz, g, gtilda, FFTW_FORWARD, FFTW_ESTIMATE);
   s = fftw_plan_dft_3d(lx, ly, lz, ctilda, c, FFTW_BACKWARD, FFTW_ESTIMATE);

   // resume = 0 - Start calculation from the beginning
   // resume = 1 - Resume calculation

   if (resume == 0)
   {
      for (z = 0; z < lx; z++)
      {
         for (y = 0; y < ly; y++)
         {
            for (x = 0; x < lz; x++)
            {
               ij = x * ly * lz + y * lz + z;

               c[ij] = c_avg;
            }
         }
      }
   }
   else
   {
      // Loading initial composition
   }


   /* Defining initial composition */

   double **random_numA, **random_numB, **random_numC, **random_numD;
   float  gasdev(long *idum);
   double rsum1, rmean1, rsum2, rmean2, rsum3, rmean3, rsum4, rmean4;

   /* Calculating spinodal points */

   pp1 = (-6 * bb + sqrt(36 * bb * bb - 96 * aa * cc)) / (24 * aa);
   pp2 = (-6 * bb - sqrt(36 * bb * bb - 96 * aa * cc)) / (24 * aa);

   // printf("\n pp1=%lf pp2= %lf", pp1, pp2);

   /* For region inside spinodal */

   if ((c_avg >= pp1) || (c_avg <= pp2))

   {

      long int SEED  = rand();
      long int SEED2 = rand();
      long int SEED3 = rand();
      long int SEED4 = rand();

      random_numA = dmatrix(0, lx, 0, ly);
      random_numB = dmatrix(0, lx, 0, ly);
      random_numC = dmatrix(0, lx, 0, ly);
      random_numD = dmatrix(0, lx, 0, ly);

      for (i = 0; i < lx; ++i)
      {
         for (j = 0; j < ly; ++j)
         {
            ij = i * ly + j;

            random_numA[i][j] = 0.00;
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

      for (z = 0; z < lx; z++)
      {
         for (y = 0; y < ly; y++)
         {
            for (x = 0; x < lz; x++)
            {

               ij = x * ly * lz + y * lz + z;

               c[ij] += random_numA[x][y] - rmean1;
               c[ij] += random_numB[x][y] - rmean2;
               c[ij] += random_numC[x][y] - rmean3;
               c[ij] += random_numD[x][y] - rmean4;
            }
         }
      }

      free_dmatrix(random_numA, 0, lx, 0, ly);
      free_dmatrix(random_numB, 0, lx, 0, ly);
      free_dmatrix(random_numC, 0, lx, 0, ly);
      free_dmatrix(random_numD, 0, lx, 0, ly);

      delkx = 2.0 * pi / (lx * delx);
      delky = 2.0 * pi / (ly * dely);
      delkz = 2.0 * pi / (lz * delz);

      halflx = (int)lx / 2.0;
      halfly = (int)ly / 2.0;
      halflz = (int)lz / 2.0;

      /* Running the code for given time */

      total_time_steps = ((total_time) / delt);

      for (n = 1; n <= total_time_steps; ++n)
      {

      /* Saving data to files */

         time = n * delt;
         if (fmod(time, time_interval) == 0)
         {
            /* Creating a file and Getting data from input file */

            char file_name[25];

            // sprintf(file_name, "Output/output_%.0f.vtk", time);

            sprintf(file_name, "Output/Data/output_%.2f.dat", time);

            FILE *fptr;
            fptr = fopen(file_name, "w");

            // fprintf(fptr, "# vtk DataFile Version 3.0\n");
            // fprintf(fptr, "Order Parameter data\n");
            // fprintf(fptr, "ASCII\n");
            // fprintf(fptr, "DATASET STRUCTURED_POINTS\n");
            // fprintf(fptr, "DIMENSIONS %d %d %d\n", lx, ly, lz);
            // fprintf(fptr, "ORIGIN 0 0 0\n");
            // fprintf(fptr, "SPACING 1 1 1\n");
            // fprintf(fptr, "POINT_DATA %d\n", lx * ly * lz);
            // fprintf(fptr, "SCALARS order_parameter double\n");
            // fprintf(fptr, "LOOKUP_TABLE default\n");

            for (z = 0; z < lx; z++)
            {
               for (y = 0; y < ly; y++)
               {
                  for (x = 0; x < lz; x++)
                  {

                     ij = x * ly * lz + y * lz + z;

                     {
                        fprintf(fptr, "%le\n", creal(c[ij]));
                     }
                  }
               }
            }
            fclose(fptr);
         }

         /* Defining free energy */

         for (z = 0; z < lx; z++)
         {
            for (y = 0; y < ly; y++)
            {
               for (x = 0; x < lz; x++)
               {

                  ij = x * ly * lz + y * lz + z;

                  g[ij] = -(4 * aa * (c[ij]) * (c[ij]) * (c[ij]) + 3 * bb * (c[ij]) * (c[ij]) + 2 * cc * (c[ij]) + dd); // Derivative of  free energy 
               }
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

               for (kk = 0; kk < lz; ++kk)
               {
                  if (kk < halflz)
                  {
                     kfz = kk * delkz;
                  }

                  else
                  {
                     kfz = (kk - lz) * delkz;
                  }
                  kfz2 = kfz * kfz;

                  k2 = kfx2 + kfy2 + kfz2;
                  k4 = k2 * k2;

                  ctilda[kk * ly * lx + j * lx + i] = 1. * (ctilda[kk * ly * lx + j * lx + i] + delt * k2 * gtilda[kk * ly * lx + j * lx + i]) / (1.0 + delt * k4);
               }
            }
         }

         /* IFFT of final composition */

         fftw_execute(s);

         /* Normalization of composition */

         for (z = 0; z < lx; z++)
         {
            for (y = 0; y < ly; y++)
            {
               for (x = 0; x < lz; x++)
               {

                  ij = x * ly * lz + y * lz + z;

                  c[ij] = 1. * c[ij] / (lx * ly * lz); 
               }
            }
         }


         /* Noise generation upto 1000 time steps */

         if (n <= 1000)

         {

            long int SEED = rand();
            long int SEED2 = rand();
            long int SEED3 = rand();
            long int SEED4 = rand();

            random_numA = dmatrix(0, lx, 0, ly);
            random_numB = dmatrix(0, lx, 0, ly);
            random_numC = dmatrix(0, lx, 0, ly);
            random_numD = dmatrix(0, lx, 0, ly);

            for (i = 0; i < lx; ++i)
            {
               for (j = 0; j < ly; ++j)
               {
                  ij = i * ly + j;

                  random_numA[i][j] = 0.00;
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

            for (z = 0; z < lx; z++)
            {
               for (y = 0; y < ly; y++)
               {
                  for (x = 0; x < lz; x++)
                  {

                     ij = x * ly * lz + y * lz + z;

                     c[ij] += random_numA[x][y] - rmean1;
                     c[ij] += random_numB[x][y] - rmean2;
                     c[ij] += random_numC[x][y] - rmean3;
                     c[ij] += random_numD[x][y] - rmean4;
                  }
               }
            }

            free_dmatrix(random_numA, 0, lx, 0, ly);
            free_dmatrix(random_numB, 0, lx, 0, ly);
            free_dmatrix(random_numC, 0, lx, 0, ly);
            free_dmatrix(random_numD, 0, lx, 0, ly);
         }
      }
   }


   /* For region outside spinodal */

   if ((c_avg <= pp1) && (c_avg >= pp2))

   {

      for (z = 0; z < lx; z++)
      {
         for (y = 0; y < ly; y++)
         {
            for (x = 0; x < lz; x++)
            {

               ij = x * ly * lz + y * lz + z;

               {
                  c[ij] = c_avg + (-1 + 2 * ((double)rand() / (double)RAND_MAX)) / 200; 
               }
            }
         }
      }

      delkx = 2.0 * pi / (lx * delx);
      delky = 2.0 * pi / (ly * dely);
      delkz = 2.0 * pi / (lz * delz);

      halflx = (int)lx / 2.0;
      halfly = (int)ly / 2.0;
      halflz = (int)lz / 2.0;

      /* Running the code for given time */

      total_time_steps = ((total_time) / delt);

      for (n = 1; n <= total_time_steps; ++n)
      {

      /* Saving data to files */ 

         time = n * delt;
         if (fmod(time, time_interval) == 0)
         {
            /* Creating a file and Getting data from input file */

            char file_name[25];

            // sprintf(file_name, "Output/output_%.0f.vtk", time);

            sprintf(file_name, "Output/Data/output_%.2f.dat", time);

            FILE *fptr;
            fptr = fopen(file_name, "w");

            // fprintf(fptr, "# vtk DataFile Version 3.0\n");
            // fprintf(fptr, "Order Parameter data\n");
            // fprintf(fptr, "ASCII\n");
            // fprintf(fptr, "DATASET STRUCTURED_POINTS\n");
            // fprintf(fptr, "DIMENSIONS %d %d %d\n", lx, ly, lz);
            // fprintf(fptr, "ORIGIN 0 0 0\n");
            // fprintf(fptr, "SPACING 1 1 1\n");
            // fprintf(fptr, "POINT_DATA %d\n", lx * ly * lz);
            // fprintf(fptr, "SCALARS order_parameter double\n");
            // fprintf(fptr, "LOOKUP_TABLE default\n");

            for (z = 0; z < lx; z++)
            {
               for (y = 0; y < ly; y++)
               {
                  for (x = 0; x < lz; x++)
                  {

                     ij = x * ly * lz + y * lz + z;

                     {
                        fprintf(fptr, "%le\n", creal(c[ij]));
                     }
                  }
               }
            }
             fclose(fptr);
         }

         /* Defining free energy */

         for (z = 0; z < lx; z++)
         {
            for (y = 0; y < ly; y++)
            {
               for (x = 0; x < lz; x++)
               {

                  ij = x * ly * lz + y * lz + z;

                  g[ij] = -(4 * aa * (c[ij]) * (c[ij]) * (c[ij]) + 3 * bb * (c[ij]) * (c[ij]) + 2 * cc * (c[ij]) + dd); // Derivative of  free energy 
               }
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

               for (kk = 0; kk < lz; ++kk)
               {
                  if (kk < halflz)
                  {
                     kfz = kk * delkz;
                  }

                  else
                  {
                     kfz = (kk - lz) * delkz;
                  }
                  kfz2 = kfz * kfz;

                  k2 = kfx2 + kfy2 + kfz2;
                  k4 = k2 * k2;

                  ctilda[kk * ly * lx + j * lx + i] = 1. * (ctilda[kk * ly * lx + j * lx + i] + delt * k2 * gtilda[kk * ly * lx + j * lx + i]) / (1.0 + delt * k4); 
               }
            }
         }

         /* IFFT of final composition */

         fftw_execute(s);

         /* Normalization of composition */

         for (z = 0; z < lx; z++)
         {
            for (y = 0; y < ly; y++)
            {
               for (x = 0; x < lz; x++)
               {

                  ij = x * ly * lz + y * lz + z;

                  c[ij] = 1. * c[ij] / (lx * ly * lz); 
               }
            }
         }
      }
   }

   fftw_free(c);
   fftw_free(g);

   fftw_destroy_plan(p);
   fftw_destroy_plan(q);
   fftw_destroy_plan(s);

   fftw_cleanup();

   return 0;
}
