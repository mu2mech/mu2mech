#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include <fftw3.h>
#include <math.h>
/*#include <unistd.h>*/
/*#include <limits.h>*/
#define pi 3.14159265

int main()

 {

   /* Data initialization */

   int    lx, x, n, i, total_time_steps, num;
   double delt, delx, k, Dtilda, delk, halflx, kf, k2, k4;
   char   junk[100];
   double time, time_interval, total_time, resume_from;
   int    resume;
   char   resume_from_str[10];

   /* Creating a file and Getting data from input file */

   FILE *fp;
   fp = fopen("Sources/input.dat", "r");

   if (fp == NULL)
   {
      printf("Cannot open file");
   }

   fscanf(fp, "\
   %s%d\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%lf\
   %s%d\
   %s%s",
          junk, &lx,
          junk, &delt,
          junk, &k,
          junk, &delx,
          junk, &Dtilda,
          junk, &time_interval,
          junk, &total_time,
          junk, &resume,
          junk, &resume_from_str);

   fclose(fp);
   sscanf(resume_from_str, "%lf", &resume_from);

   /* Defining variables in fourier space */

   fftw_complex *c, *ctilda, *g, *gtilda;

   c      = fftw_malloc(sizeof(fftw_complex) * lx);
   ctilda = fftw_malloc(sizeof(fftw_complex) * lx);
   g      = fftw_malloc(sizeof(fftw_complex) * lx);
   gtilda = fftw_malloc(sizeof(fftw_complex) * lx);

   /* Defining FFT Plans */

   fftw_plan p, q, s;

   p = fftw_plan_dft_1d(lx, c, ctilda, FFTW_FORWARD, FFTW_ESTIMATE);
   q = fftw_plan_dft_1d(lx, g, gtilda, FFTW_FORWARD, FFTW_ESTIMATE);
   s = fftw_plan_dft_1d(lx, ctilda, c, FFTW_BACKWARD, FFTW_ESTIMATE);

   /* Defining initial composition */

   for (x = 0; x < lx; ++x)

   {
      if ((x >= 0) && (x < lx / 2))
       {
         c[x] = 1;
       }

      else
      {
         c[x] = -1;
      }
   }

   delk   = 2.0 * pi / (lx * delx);
   halflx = (int)lx / 2.0;

   /* Running the code for given time */

   total_time_steps = ((total_time) / delt);
   n                = ((resume_from) / delt) + 1;

   for (n = 1; n <= total_time_steps; ++n)
   {

      /* Defining free energy derivative (f=1/4(c^2-1)^2)*/

      for (x = 0; x < lx; ++x)
      {
         g[x] = -(c[x]) * (c[x] - 1) * (1 + c[x]);
      }

      /* FFT of composition and  free energy */

      fftw_execute(q);
      fftw_execute(p);

      for (i = 0; i < lx; ++i)
      {
         if (i < halflx)
         {
            kf = i * delk;
         }

         else
         {
            kf = (i - lx) * delk;
         }

         k2 = kf * kf;
         k4 = k2 * k2;

         ctilda[i] = 1. * (ctilda[i] + Dtilda * delt * k2 * gtilda[i]) / (1.0 + k * delt * k4); 
      }

      /* IFFT of final composition */

      fftw_execute(s);

      /* Normalization of composition */

      for (i = 0; i < lx; ++i)
      {
         c[i] = 1. * c[i] / (lx); 
      }

      // Saving data to files
      time = n * delt;

      if (fmod(time, time_interval) == 0 )
      {
         char file_name[25];
         sprintf(file_name, "Output/Data/output_%.2f.dat", time);
         FILE *fptr;
         fptr = fopen(file_name, "w");

         for (x = 0; x < lx; ++x)
         {
            fprintf(fptr, "%d %f\n", x, creal(c[x]));
         }
         fclose(fptr);
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
