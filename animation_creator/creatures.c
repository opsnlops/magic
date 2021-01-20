
#include <stdio.h>
#include <stdint.h>

#include "creatures.h"

// Write out the file with our magic number
FILE *open_file(char *file_name, struct Header header)
{
    FILE *our_file = fopen(file_name, "wb");
    fwrite(MAGIC_NUMBER, sizeof(MAGIC_NUMBER), 1, our_file);
    fwrite(&header, sizeof(header), 1, our_file);
    return our_file;
}

// Close the file cleanly
void close_file(FILE *file)
{
    fclose(file);
}

// Write out a movement frame to disk
void write_movement_frame(FILE *file, uint8_t *positions, int number_of_servos)
{
    putc(MOVEMENT_FRAME_TYPE, file);
    fwrite(positions, number_of_servos, 1, file);
}