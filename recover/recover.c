#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover FILE\n");
        return 1;
    }

    // Open forensic image for reading
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s for reading.\n", argv[1]);
        return 1;
    }

    // Buffer to store 512 bytes
    uint8_t buffer[512];

    // Counter for JPEG filenames
    int jpeg_count = 0;

    // File pointer for JPEGs
    FILE *jpeg = NULL;

    // Read the forensic image block by block
    while (fread(buffer, sizeof(uint8_t), 512, file) == 512)
    {
        // Check for the start of a new JPEG
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // If a JPEG is already open, close it
            if (jpeg != NULL)
            {
                fclose(jpeg);
            }

            // Create a new JPEG file
            char filename[8];
            sprintf(filename, "%03d.jpg", jpeg_count);
            jpeg = fopen(filename, "w");
            if (jpeg == NULL)
            {
                fprintf(stderr, "Could not create %s.\n", filename);
                fclose(file);
                return 1;
            }

            // Increment the JPEG count
            jpeg_count++;
        }

        // Write the block to the current JPEG
        if (jpeg != NULL)
        {
            fwrite(buffer, sizeof(uint8_t), 512, jpeg);
        }
    }

    // Close any remaining files
    if (jpeg != NULL)
    {
        fclose(jpeg);
    }

    // Close the forensic image
    fclose(file);

    return 0;
}
