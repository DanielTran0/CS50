#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    // Checks for a single command line argument
    if (argc != 2)
    {
        printf("Only one command line argument allowed\n");
        return 1;
    }

    // Opens memory card to read from
    FILE *mcard = fopen(argv[1], "r");
    if (mcard == NULL)
    {
        printf("Could not open file\n");
        return 1;
    }

    // Creates an array to read memory card to
    uint8_t buf[512];
    FILE *pic;
    char name[7];
    int counter = 0;


    while (fread(&buf, 512, 1, mcard))
    {
        // Checks to see if it is a jpeg
        if (buf[0] == 0xff && buf[1] == 0xd8 && buf[2] == 0xff && (buf[3] & 0xf0) == 0xe0)
        {
            // If a jpeg is open close it
            if (counter > 0)
            {
                fclose(pic);
            }

            // Creates a counting name for a jpeg
            sprintf(name, "%03i.jpg", counter);

            // Opens a new file for a jpeg
            pic = fopen(name, "w");
            if (pic == NULL)
            {
                printf("Could not open file\n");
                return 1;
            }
            counter++;
        }

        // If jpeg is open write to it
        if (counter > 0)
        {
            fwrite(&buf, 512, 1, pic);
        }
    }
    fclose(mcard);
    fclose(pic);
}