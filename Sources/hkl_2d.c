#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int minimum(int p_left, int p_down, int p_right, int p_up);
int maximum(int p_left, int p_down, int p_right, int p_up);

int main()
{

    int ijk, j, i1, i2, i3, nx, ny, list = 1, interval = 1;
    FILE *fpr, *fpw;
    double tmpelement;
    char ch[50], NAME[50];
    double v_frac[list];
    int p, right, left, up, back, down, front, a, b, c, d, e, f;
    int volume[200000];
    int iplus, iminus, jplus, jminus;
    int iplus2, iminus2, jplus2, jminus2;
    int g_left;
    int g_down;
    int g_right;
    int g_up;
    char junk[100];
    float i;

    double radius[50000];
    double x, y;
    int label, g, kij;
    int j1, j2;
    int a1, a2, a3, m1;
    int b1, b2, b3, m2;
    int c1, c2, c3, m3;
    int equal, max;
    double r_avg;
    double delt = 1;
    double delx = 1;

    /* Creating a file and Getting data from input file */
    FILE *fp;
    fp = fopen("input.dat", "r");
    if (fp == NULL)
    {
        printf("Cannot open file");
    }
    fscanf(fp, "\
   %s%d\
   %s%d\
   %s%f",
           junk, &nx,
           junk, &ny,
           junk, &i);
    fclose(fp);


    double *comp = (double *)malloc(nx * ny * sizeof(double));
    int *particle = (int *)malloc(nx * ny * sizeof(int));

    sprintf(ch, "./Output/Data/output_%0.2f.dat", i);

    if ((fpr = fopen(ch, "r")) == NULL)
    {
        printf("Unable to open file %s", ch);
        printf("Exiting\n");
        exit(0);
    }
    else
    {
        fpw = fopen(ch, "r");
    }

    for (i1 = 0; i1 < nx; ++i1)
    {
        for (i2 = 0; i2 < ny; ++i2)
        {

            ijk = i2 + i1 * ny;
            particle[ijk] = 0;

            fscanf(fpr, "%lf ", &comp[ijk]);
        }
        fscanf(fpr, "\n");
    }
    fclose(fpr);

    p = 1;

    for (i1 = 0; i1 < nx; ++i1)
    {
        for (i2 = 0; i2 < ny; ++i2)
        {

            ijk = i2 + i1 * ny;

            iplus = (i1 + 1 + nx) % nx;
            jplus = (i2 + 1 + ny) % ny;
            iminus = ((i1 - 1) + nx) % nx;
            jminus = ((i2 - 1) + ny) % ny;

            left = i2 + (iminus)*ny;
            right = i2 + (iplus)*ny;
            up = (jplus) + i1 * ny;
            down = (jminus) + i1 * ny;

            if ((comp[ijk] > 0.5) && (particle[ijk] == 0))
            {
                g_left = particle[left];
                g_down = particle[down];
                if ((particle[down] != 0) || (particle[left] != 0) || (particle[up] != 0) || (particle[right] != 0))
                {
                    particle[ijk] = minimum(g_left, g_down, g_right, g_up);
                }
                else
                {
                    particle[ijk] = p;
                    p = p + 1;
                }
            }
        }
    }

    for (i1 = 0; i1 < nx; ++i1)
    {
        for (i2 = 0; i2 < ny; ++i2)
        {

            ijk = i2 + i1 * ny;
            iplus = (i1 + 1 + nx) % nx;
            jplus = (i2 + 1 + ny) % ny;

            iminus = ((i1 - 1) + nx) % nx;
            jminus = ((i2 - 1) + ny) % ny;

            left = i2 + (iminus)*ny;
            right = i2 + (iplus)*ny;
            up = (jplus) + i1 * ny;
            down = (jminus) + i1 * ny;

            equal = particle[ijk];
            if (particle[ijk] > 0)
            {
                g_left = particle[left];
                g_down = particle[down];
                g_right = particle[right];
                g_up = particle[up];

                max = minimum(g_left, g_down, g_right, g_up);

                if ((particle[down] != 0) || (particle[left] != 0) || (particle[up] != 0) || (particle[right] != 0))
                {
                    if (equal > max)
                    {
                        g = g + 1;
                        label = minimum(g_left, g_down, g_right, g_up);

                        for (a1 = 0; a1 < nx; ++a1)
                        {
                            for (a2 = 0; a2 < ny; ++a2)
                            {

                                m1 = a2 + a1 * ny;
                                if (particle[m1] == equal)
                                {
                                    particle[m1] = label;
                                }
                            }
                        }
                    }
                }
            }
        }
    }

    for (a = 1; a < p; ++a)
    {
        volume[a] = 0;

        for (i1 = 0; i1 < nx; ++i1)
        {
            for (i2 = 0; i2 < ny; ++i2)
            {

                ijk = i2 + i1 * ny;
                if (particle[ijk] == a)
                {
                    volume[a] = volume[a] + 1;
                }
            }
        }
    }

    sprintf(NAME, "./Output/PostData/volume_%0.2f.dat", i);
    if ((fpw = fopen(NAME, "w")) == NULL)
    {
        printf("Unable to open file %s", NAME);
        printf("Exiting\n");
        exit(0);
    }
    else
    {
        fpw = fopen(NAME, "w");
    }

    b1 = 0;
    for (a = 1; a < p; ++a)
    {
        if (volume[a] > 0)
        {
            b1 = b1 + 1;
            tmpelement = (volume[a] / (M_PI));
            radius[a] = delx * pow(tmpelement, 1 / 2.0);
            r_avg = r_avg + radius[a];
            fprintf(fpw, "%d %d %d %lf\n", b1, a, volume[a], radius[a]);
        }
    }

    fclose(fpw);

    r_avg = r_avg / b1;
    sprintf(NAME, "./Output/PostData/avg_rad_%0.2f.dat", i);
    if ((fpw = fopen(NAME, "a")) == NULL)
    {
        printf("Unable to open file %s", NAME);
        printf("Exiting\n");
        exit(0);
    }
    else
    {
        fpw = fopen(NAME, "a");
    }

    fprintf(fpw, "%lf %lf %lf %d\n", i * delt, r_avg, r_avg * r_avg * r_avg * r_avg, b1);

    fclose(fpw);

    // printf("%d",p);
    // i = i + interval;
    // 	free(comp);
    // free(particle);
}

// PROGRAM ENDS

int minimum(int p_left, int p_down, int p_right, int p_up)
{
    int min1, min2, min3, i, j;

    int min[6];
    min[0] = p_left;
    min[1] = p_down;
    min[2] = p_right;
    min[3] = p_up;

    for (i = 0; i < 4; ++i)
    {
        for (j = i + 1; j < 4; ++j)
        {
            if (min[i] > min[j])
            {
                min1 = min[i];
                min[i] = min[j];
                min[j] = min1;
            }
        }
    }

    if (min[0] > 0)
    {
        min2 = min[0];
    }
    else if (min[1] > 0)
    {
        min2 = min[1];
    }
    else if (min[2] > 0)
    {
        min2 = min[2];
    }

    else
    {
        min2 = min[3];
    }

    // printf("%d\t%d\t%d\t%d\n",min[0],min[1],min[2],min2);
    return (min2);
}