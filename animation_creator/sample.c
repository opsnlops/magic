
#include <stdio.h>
#include <stdint.h>
#include <string.h>

struct Header
{
    uint8_t version;
    uint8_t number_of_servos;
    uint16_t number_of_frames;
    uint16_t time_per_frame; // Number of milliseconds for each frame
} header;

void make_frames(uint8_t *frames, int number_of_servos, int number_of_frames)
{
    int frameNumber = 0;
    int position = 0;
    for (int frame = 0; frame < number_of_frames; frame++)
    {
        printf("working on frame %d\n", frame);
        for (int servo = 0; servo < number_of_servos; servo++)
        {
            frames[position++] = (uint8_t)frame;
        }

        frameNumber++;
    }
}

int main()
{
    header.version = (uint8_t)1;
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
    fwrite(&header, sizeof(header), 1, sample_file);
    fwrite(&frames, sizeof(frames), 1, sample_file);
    fclose(sample_file);

    return 0;
}