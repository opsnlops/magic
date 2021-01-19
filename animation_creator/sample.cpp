
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <list>

#include "creatures.h"

uint16_t number_of_frames = (uint16_t)240;
uint8_t number_of_servos = (uint8_t)4;
uint16_t time_per_frame = (uint16_t)50;

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
    Header *header = new Header(number_of_servos, number_of_frames, time_per_frame);

    int size = sizeof(header);

    std::list<uint8_t> data = {(uint8_t)1, (uint8_t)2, (uint8_t)3, (uint8_t)4};

    Frame frame = Frame();
    frame.data = data;

    std::list<uint8_t> frames;

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