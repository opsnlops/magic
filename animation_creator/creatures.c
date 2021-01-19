
#include <stdio.h>
#include <stdint.h>

#include "creatures.h"

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