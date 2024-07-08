#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <fftw3.h>
#include <time.h>
#include <math.h>
#include <stdlib.h>
#include "nrutil.c"
#include "gasdev.c"
#define pi 3.14159265

/* Evolution of microstructure of composition in spinoidal range */
/* Order of fluctuation or noise added */
/* Flag is added */

int main()
{

   /* Data initialization */
   int lx, ly, M, k, x, y, n, N, i, j, ij, m, total_time_time_interval;
   double delt, total_time, delkx, delky, halflx, halfly, kfx, kfy, kfx2, kfy2, k2, k4, delx, dely, c_avg, fluctuation;
   char junk[100];

   char NAME[50];
   double time_interval = 100; // time_interval after which composition need to be printed//
   double time;
   int resume;
   char resume_from_str[10];
   double resume_from;

   double aa, bb, cc, dd, ee, pp1, pp2, Ag, Hg; /* G = a*C^4 + b*C^3 + c*C^2 + d*C + e ,p1 and p2 are spinodal points*/

   /* Creating a file and Getting data from input file */
   FILE *fptr;
   FILE *fptr8;
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
          junk, &Ag,
          junk, &Hg,
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

   // printf("%lf\n", dely);
   // printf("%lf\n", time_interval);
   // printf("%lf\n", total_time);
   // printf("%d\n", resume);
   // printf("%s\n", resume_from_str);

   fftw_complex *c, *ctilda, *g, *gtilda, *M1, *f1x, *f1y, *f1tildax, *f1tilday, *f2x, *f2y, *f2tildax, *f2tilday;
   fftw_plan p, q, q1x, q2x, q1y, q2y, s;

   c = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   ctilda = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   g = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   gtilda = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   M1 = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   f1x = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   f1tildax = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   f2x = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   f2tildax = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   f1y = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   f1tilday = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   f2y = fftw_malloc(sizeof(fftw_complex) * lx * ly);
   f2tilday = fftw_malloc(sizeof(fftw_complex) * lx * ly);

   p = fftw_plan_dft_2d(lx, ly, c, ctilda, FFTW_FORWARD, FFTW_ESTIMATE);
   q = fftw_plan_dft_2d(lx, ly, g, gtilda, FFTW_FORWARD, FFTW_ESTIMATE);
   s = fftw_plan_dft_2d(lx, ly, ctilda, c, FFTW_BACKWARD, FFTW_ESTIMATE);
   q1x = fftw_plan_dft_2d(lx, ly, f2x, f2tildax, FFTW_FORWARD, FFTW_ESTIMATE);
   q2x = fftw_plan_dft_2d(lx, ly, f1tildax, f1x, FFTW_BACKWARD, FFTW_ESTIMATE);
   q1y = fftw_plan_dft_2d(lx, ly, f2y, f2tilday, FFTW_FORWARD, FFTW_ESTIMATE);
   q2y = fftw_plan_dft_2d(lx, ly, f1tilday, f1y, FFTW_BACKWARD, FFTW_ESTIMATE);

   /* Defining initial composition */

   double **random_numA, **random_numB, **random_numC, **random_numD;
   float gasdev(long *idum);
   double rsum1, rmean1, rsum2, rmean2, rsum3, rmean3, rsum4, rmean4;

   if (resume == 0)
   {
      /* Defining initial composition */
      /* Providing noise from -0.001 to +0.001*/

      for (i = 0; i < lx; ++i)
      {
         for (j = 0; j < ly; ++j)
         {
            ij = i * ly + j;

            c[ij] = c_avg;
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

   /* Saving initial profile*/

   // sprintf(NAME, "output/comp0.txt");
   // fptr = fopen(NAME, "w");

   // for (i = 0; i < lx; i++)
   // {
   //    for (j = 0; j < ly; j++)
   //    {
   //       ij = ly * i + j;
   //       fprintf(fptr, "%lf ", creal(c[ij]));
   //    }
   //    fprintf(fptr, "\n");
   // }
   // fclose(fptr);

   /* for fe-Cr at 400 C */

   /*
   aa=1;
   bb=-2.041;
   cc=1.2214;
   dd=-0.1837;
   ee=0.0081;
   */


   /* for fe-Cu at 1300 C

   aa=1;
   bb=-1.76;
   cc= 0.9504;
   dd=-0.1458;
   ee=0.0077;
   */

   pp1 = (-6 * bb + sqrt(36 * bb * bb - 96 * aa * cc)) / (24 * aa);
   pp2 = (-6 * bb - sqrt(36 * bb * bb - 96 * aa * cc)) / (24 * aa);

   printf("\n pp1=%lf pp2= %lf", pp1, pp2);

   int rand1, rand2, rand3, rand4;

   rand1 = rand();
   rand2 = rand();
   rand3 = rand();
   rand4 = rand();

   if ((c_avg >= pp1) || (c_avg <= pp2))

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

      for (x = 0; x < lx; ++x)
      {
         for (y = 0; y < ly; ++y)
         {

            {
               c[y + ly * x] = c[y + ly * x] + (-1 + 2 * ((double)rand() / (double)RAND_MAX)) / 10; /* ((double)rand()/(double)RAND_MAX) generates the random no. between 0 and 1*/
            }
         }
      }

      delkx = 2.0 * pi / (lx * delx);
      delky = 2.0 * pi / (ly * dely);

      halflx = (int)lx / 2.0;
      halfly = (int)ly / 2.0;

      /* Running the code for given time */
      total_time_time_interval = ((total_time) / delt);

      for (n = 1; n <= total_time_time_interval; ++n)
      {

         /* Defining free energy */

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)
            {

               g[y + ly * x] = -(Ag / Hg) * (4 * aa * (c[y + ly * x]) * (c[y + ly * x]) * (c[y + ly * x]) + 3 * bb * (c[y + ly * x]) * (c[y + ly * x]) + 2 * cc * (c[y + ly * x]) + dd); /* Derivative of  free energy */
                                                                                                                                                                                         // M1[y+ly*x] = fabs(1/(12*aa*(c[y+ly*x])*(c[y+ly*x]) + 6*bb*(c[y+ly*x])+ 2*cc));
               M1[y + ly * x] = (c[y + ly * x]) * (1 - c[y + ly * x]);
            }
         }

         printf("time is = %lf\n", n * delt);

         /* FFT of composition and  free energy */

         fftw_execute(q);
         fftw_execute(p);

         for (x = 0; x < lx; ++x)
         {
            if (x < halflx)
            {
               kfx = x * delkx;
            }

            else
            {
               kfx = (x - lx) * delkx;
            }
            kfx2 = kfx * kfx;

            for (y = 0; y < ly; ++y)
            {
               if (y < halfly)
               {
                  kfy = y * delky;
               }

               else
               {
                  kfy = (y - ly) * delky;
               }

               kfy2 = kfy * kfy;
               k2 = kfx2 + kfy2;
               k4 = k2 * k2;

               f1tildax[y + ly * x] = _Complex_I * (kfx) * (gtilda[y + ly * x] + k2 * ctilda[y + ly * x]);
               f1tilday[y + ly * x] = _Complex_I * (kfy) * (gtilda[y + ly * x] + k2 * ctilda[y + ly * x]);
            }
         }

         fftw_execute(q2x);
         fftw_execute(q2y);

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)
            {

               f1x[y + ly * x] = 1. * f1x[y + ly * x] / (lx * ly);
               f1y[y + ly * x] = 1. * f1y[y + ly * x] / (lx * ly);

               // printf("f1 is = %lf ", creal(f1[y+ly*x]));
            }
         }

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)
            {

               f2x[y + ly * x] = creal(f1x[y + ly * x]) * M1[y + ly * x];
               f2y[y + ly * x] = creal(f1y[y + ly * x]) * M1[y + ly * x];
            }
         }

         fftw_execute(q1x);
         fftw_execute(q1y);

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

               ctilda[j + ly * i] = 1. * (((1 + 0.5 * delt * k4) * ctilda[j + ly * i] + delt * (f2tildax[j + ly * i] * kfx + f2tilday[j + ly * i] * kfy) * _Complex_I) / (1 + 0.5 * delt * k4)); /* no need need to define new variable and replace ctilda values */
            }
         }

         // saving data files

         /* saving composition in 2D */
         time = n * delt;
         if (fmod(time, time_interval) == 0)
         {
            sprintf(NAME, "Output/Data/output_%.2f.dat", n * delt);
            fptr = fopen(NAME, "w");

            for (i = 0; i < lx; i++)
            {
               for (j = 0; j < ly; j++)
               {
                  ij = ly * i + j;
                  fprintf(fptr, "%lf ", creal(c[ij]));
               }
               fprintf(fptr, "\n");
            }
            fclose(fptr);
         }

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

      printf("\nenter the total time\n");
      // scanf("%lf", &total_time);
      printf("%lf", total_time);

      total_time_time_interval = ((total_time) / delt);

      for (n = 1; n <= total_time_time_interval; ++n)
      {

         /* Defining free energy */

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)
            {
               // g[y+ly*x]=  (4*aa*(c[y+ly*x])*(c[y+ly*x])*(c[y+ly*x]) + 3*bb*(c[y+ly*x])*(c[y+ly*x]) + 2*cc*(c[y+ly*x]) +dd);
               g[y + ly * x] = (Ag / Hg) * (4 * aa * (c[y + ly * x]) * (c[y + ly * x]) * (c[y + ly * x]) + 3 * bb * (c[y + ly * x]) * (c[y + ly * x]) + 2 * cc * (c[y + ly * x]) + dd);
               // M1[y+ly*x] = fabs(1/(12*aa*(c[y+ly*x])*(c[y+ly*x]) + 6*bb*(c[y+ly*x])+ 2*cc));
               M1[y + ly * x] = (c[y + ly * x]) * (1 - c[y + ly * x]);
            }
         }

         printf("time is = %lf\n", n * delt);

         /* FFT of composition and  free energy */

         fftw_execute(q);
         fftw_execute(p);

         for (x = 0; x < lx; ++x)
         {
            if (x < halflx)
            {
               kfx = x * delkx;
            }

            else
            {
               kfx = (x - lx) * delkx;
            }
            kfx2 = kfx * kfx;

            for (y = 0; y < ly; ++y)
            {
               if (y < halfly)
               {
                  kfy = y * delky;
               }

               else
               {
                  kfy = (y - ly) * delky;
               }

               kfy2 = kfy * kfy;
               k2 = kfx2 + kfy2;
               k4 = k2 * k2;

               f1tildax[y + ly * x] = _Complex_I * (kfx) * (gtilda[y + ly * x] + k2 * ctilda[y + ly * x]);
               f1tilday[y + ly * x] = _Complex_I * (kfy) * (gtilda[y + ly * x] + k2 * ctilda[y + ly * x]);
            }
         }

         fftw_execute(q2x);
         fftw_execute(q2y);

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)
            {

               f1x[y + ly * x] = 1. * f1x[y + ly * x] / (lx * ly);
               f1y[y + ly * x] = 1. * f1y[y + ly * x] / (lx * ly);

               // printf("f1 is = %lf ", creal(f1[y+ly*x]));
            }
         }

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)
            {

               f2x[y + ly * x] = creal(f1x[y + ly * x]) * M1[y + ly * x];
               f2y[y + ly * x] = creal(f1y[y + ly * x]) * M1[y + ly * x];
            }
         }

         fftw_execute(q1x);
         fftw_execute(q1y);

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

               ctilda[j + ly * i] = 1. * (((1 + 0.5 * delt * k4) * ctilda[j + ly * i] + delt * (f2tildax[j + ly * i] * kfx + f2tilday[j + ly * i] * kfy) * _Complex_I) / (1 + 0.5 * delt * k4)); /* no need need to define new variable and replace ctilda values */
            }
         }

         /* IFFT of final composition */

         fftw_execute(s);

         /* Normalization of composition */

         for (x = 0; x < lx; ++x)
         {
            for (y = 0; y < ly; ++y)

            {
               c[y + ly * x] = 1. * c[y + ly * x] / (lx * ly); /* can be written as c[i] *= 1./(lx*ly) */
            }
         }

         // saving data files

         /* saving composition in 2D */
         time = n * delt;
         // double m = fmod(time, time_interval);
         // printf("%d, %lf\n",n,m);
         if (fmod(time, time_interval) == 0)
         {
            sprintf(NAME, "Output/Data/output_%.2f.dat", n * delt);
            fptr = fopen(NAME, "w");

            for (i = 0; i < lx; i++)
            {
               for (j = 0; j < ly; j++)
               {
                  ij = ly * i + j;
                  fprintf(fptr, "%lf ", creal(c[ij]));
               }
               fprintf(fptr, "\n");
            }
            fclose(fptr);
         }
      }
   }

   fftw_free(c);
   fftw_free(g);
   fftw_free(M1);

   fftw_destroy_plan(p);
   fftw_destroy_plan(q);
   fftw_destroy_plan(q1x);
   fftw_destroy_plan(s);

   fftw_cleanup();

   fclose(fp);

   return 0;
}
