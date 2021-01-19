
#ifndef _APRILS_CREATURES_WAS_HERE
#define _APRILS_CREATURES_WAS_HERE

#include <stdio.h>
#include <stdint.h>

#define CREATURE_VERSION 1

#define MOVEMENT_FRAME_TYPE 1
#define PAUSE_FRAME_TYPE 2
#define LED_CONTROL_FRAME_TYPE 3

#define MAGIC_NUMBER "RAWR!"

struct Header
{
    uint8_t version;
    uint8_t number_of_servos;
    uint16_t number_of_frames;
    uint16_t time_per_frame; // Number of milliseconds for each frame
};

void make_frames(uint8_t *frames, int number_of_servos, int number_of_frames);

#endif
