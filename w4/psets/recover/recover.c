#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

typedef uint8_t BYTE;
#define BLOCK_SIZE 512

int main(int argc, char *argv[])
{
    // Check found file input
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    // open file input and check open file Done
    FILE *raw = fopen(argv[1], "r");
    if (raw == NULL)
    {
        printf("File %s not open\n", argv[1]);
        return 1;
    }

    // Delete all old jpg file current directory
    system("rm -f *.jpg");

    BYTE buffer[BLOCK_SIZE] = {0};
    int countImage = -1;
    char nameFile[8];
    FILE *image;

    while (fread(buffer, BLOCK_SIZE, 1, raw))
    {
        // check header 
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If at least one head was detected during the previous iteration
            // close image old
            if (countImage > -1)
            {
                fclose(image);
            }

            // create and open new file output
            countImage++;
            sprintf(nameFile, "%.3i.jpg", countImage);
            image = fopen(nameFile, "w");
           
            // if not open and create new file output => exit program
            if (image == NULL)
            {
                fclose(raw);
                printf("Error: not create new file jpg\n");
                return 1;
            }
        }

        // If at least one head was detected during the previous iteration
        // write output file 
        if (countImage > -1)
        {
            fwrite(buffer, BLOCK_SIZE, 1, image);
        }
    }

    // close all files
    fclose(raw);
    fclose(image);

    return 0;
}