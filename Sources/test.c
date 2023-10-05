#include <stdio.h>

void main()
{
    int lx = 10, ly = 10;
    int x, y;
    for (x = 0; x < 10; ++x)
    {
        for (y = 0; y < 10; ++y)
        {
            printf("%d %d \n", x, y);
            // g[y + ly * x] = -2 * (c[y + ly * x]) * (1 + 2 * (c[y + ly * x]) * (c[y + ly * x]) - 3 * (c[y + ly * x]));
        }
    }
}