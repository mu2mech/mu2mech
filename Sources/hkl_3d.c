#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int minimum(int p_left, int p_down, int p_back, int p_right, int p_up, int p_front);
int maximum(int p_left, int p_down, int p_back, int p_right, int p_up, int p_front);

int main()
{

    int ijk, j, i1, i2, i3, nx = 600, ny = 600, nz = 64, list = 60000, interval = 10000;
    FILE *fpr, *fpw;
    double tmpelement;
    char ch[50], NAME[50];
    double v_frac[list];
    int p, right, left, up, back, down, front, a, b, c, d, e, f;
    int volume[200000];
    int iplus, iminus, jplus, jminus, zplus, zminus;
    int iplus2, iminus2, jplus2, jminus2, zplus2, zminus2;
    int g_left;
    int g_down;
    int g_back;
    int g_right;
    int g_up;
    int g_front;
    double x, y, z;
    double radius[50000];
    double *comp = (double *)malloc(nx * ny * nz * sizeof(double));
    int *particle = (int *)malloc(nx * ny * nz * sizeof(int));
    int label, g, kij;
    int j1, j2, j3;
    int a1, a2, a3, m1;
    int b1, b2, b3, m2;
    int c1, c2, c3, m3;
    int equal, max;
    double r_avg;
    double delt = 0.01;
    double delx = 2.0;
    char junk[100];
    float i;

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
   %s%d\
   %s%f",
           junk, &nx,
           junk, &ny,
           junk, &nz,
           junk, &i);
    fclose(fp);

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
            for (i3 = 0; i3 < nz; ++i3)
            {
                ijk = i3 + i2 * nz + i1 * ny * nz;
                particle[ijk] = 0;

                fscanf(fpr, "%lf\t%lf\t%lf\t%lf\n", &x, &y, &z, &comp[ijk]);
            }
        }
    }
    fclose(fpr);

    p = 1;
    for (i1 = 0; i1 < nx; ++i1)
    {
        for (i2 = 0; i2 < ny; ++i2)
        {
            for (i3 = 0; i3 < nz; ++i3)
            {
                ijk = i3 + i2 * nz + i1 * ny * nz;
                iplus = (i1 + 1 + nx) % nx;
                jplus = (i2 + 1 + ny) % ny;
                zplus = (i3 + 1 + nz) % nz;

                iminus = ((i1 - 1) + nx) % nx;
                jminus = ((i2 - 1) + ny) % ny;
                zminus = ((i3 - 1) + nz) % nz;

                left = i3 + i2 * nz + (iminus)*ny * nz;
                right = i3 + i2 * nz + (iplus)*ny * nz;
                up = i3 + (jplus)*nz + i1 * ny * nz;
                down = i3 + (jminus)*nz + i1 * ny * nz;
                back = zminus + i2 * nz + i1 * nz * ny;
                front = zplus + i2 * nz + i1 * nz * ny;

                if ((comp[ijk] > 0.5) && (particle[ijk] == 0))
                {
                    g_left = particle[left];
                    g_down = particle[down];
                    g_back = particle[back];
                    if ((particle[down] != 0) || (particle[left] != 0) || (particle[back] != 0) || (particle[up] != 0) || (particle[right] != 0) || (particle[front] != 0))
                    {
                        particle[ijk] = minimum(g_left, g_down, g_back, g_right, g_up, g_front);
                    }
                    else
                    {
                        particle[ijk] = p;
                        p = p + 1;
                    }
                }
            }
        }
    }

    for (i1 = 0; i1 < nx; ++i1)
    {
        for (i2 = 0; i2 < ny; ++i2)
        {
            for (i3 = 0; i3 < nz; ++i3)
            {
                ijk = i3 + i2 * nz + i1 * ny * nz;
                iplus = (i1 + 1 + nx) % nx;
                jplus = (i2 + 1 + ny) % ny;
                zplus = (i3 + 1 + nz) % nz;

                iminus = ((i1 - 1) + nx) % nx;
                jminus = ((i2 - 1) + ny) % ny;
                zminus = ((i3 - 1) + nz) % nz;

                left = i3 + i2 * nz + (iminus)*ny * nz;
                right = i3 + i2 * nz + (iplus)*ny * nz;
                up = i3 + (jplus)*nz + i1 * ny * nz;
                down = i3 + (jminus)*nz + i1 * ny * nz;
                back = zminus + i2 * nz + i1 * nz * ny;
                front = zplus + i2 * nz + i1 * nz * ny;

                equal = particle[ijk];
                if (particle[ijk] > 0)
                {
                    g_left = particle[left];
                    g_down = particle[down];
                    g_back = particle[back];
                    g_right = particle[right];
                    g_up = particle[up];
                    g_front = particle[front];
                    max = minimum(g_left, g_down, g_back, g_right, g_up, g_front);
                    if ((particle[down] != 0) || (particle[left] != 0) || (particle[back] != 0) || (particle[up] != 0) || (particle[right] != 0) || (particle[front] != 0))
                    {
                        if (equal > max)
                        {
                            g = g + 1;
                            label = minimum(g_left, g_down, g_back, g_right, g_up, g_front);

                            for (a1 = 0; a1 < nx; ++a1)
                            {
                                for (a2 = 0; a2 < ny; ++a2)
                                {
                                    for (a3 = 0; a3 < nz; ++a3)
                                    {
                                        m1 = a3 + a2 * nz + a1 * ny * nz;
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
        }
    }

    for (a = 1; a < p; ++a)
    {
        volume[a] = 0;

        for (i1 = 0; i1 < nx; ++i1)
        {
            for (i2 = 0; i2 < ny; ++i2)
            {
                for (i3 = 0; i3 < nz; ++i3)
                {
                    ijk = i3 + i2 * nz + i1 * ny * nz;
                    if (particle[ijk] == a)
                    {
                        volume[a] = volume[a] + 1;
                    }
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
            tmpelement = (3.0 * volume[a] / (M_PI * 4.0));
            radius[a] = delx * pow(tmpelement, 1 / 3.0);
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

    fprintf(fpw, "%lf %lf %d\n", i * delt, r_avg, b1);

    fclose(fpw);

    free(comp);
    free(particle);
}
// PROGRAM ENDS

int minimum(int p_left, int p_down, int p_back, int p_right, int p_up, int p_front)
{
    int min1, min2, min3, i, j;

    int min[6];
    min[0] = p_left;
    min[1] = p_down;
    min[2] = p_back;
    min[3] = p_right;
    min[4] = p_up;
    min[5] = p_front;

    for (i = 0; i < 6; ++i)
    {
        for (j = i + 1; j < 6; ++j)
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
    else if (min[3] > 0)
    {
        min2 = min[3];
    }
    else if (min[4] > 0)
    {
        min2 = min[4];
    }
    else
    {
        min2 = min[5];
    }
    return (min2);
}
