
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "creatures.h"

struct Header header;

int main()
{
    header.version = (uint8_t)CREATURE_VERSION;
    header.number_of_servos = (uint8_t)4;
    header.number_of_frames = (uint16_t)240;
    header.time_per_frame = (uint16_t)22;

    int size = sizeof(header);

    uint8_t frames[header.number_of_servos * header.number_of_frames];

    // Zero out the frame buffer just in case
    memset(&frames, '\0', sizeof(frames));

    make_frames(frames, header.number_of_servos, header.number_of_frames);

    printf("The size of the header is: %d\n", size);
    printf("The size of the frames is: %ld\n", sizeof(frames));

    FILE *sample_file;
    sample_file = fopen("sample.bin", "wb");
    fwrite(MAGIC_NUMBER, sizeof(MAGIC_NUMBER), 1, sample_file);
    fwrite(&header, sizeof(header), 1, sample_file);
    fwrite(&frames, sizeof(frames), 1, sample_file);
    fclose(sample_file);

    return 0;
}