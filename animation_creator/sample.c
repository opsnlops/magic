
/**
 * Create a sample event loop
 *
 * This file will create a sample event loop called "sample.bin" for the sole
 * purpose of being a source of truth for what an actual event loop looks like.
 */

#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "creatures.h"

#define FILE_NAME "sample.bin"

/*
    Make a bunch of sample movement frames for testing. It makes the number of
    frames that are requested, with the data_to_use repeated over and over again
*/
void make_test_movement_frames(uint8_t *frames, int number_of_servos, uint8_t data_to_use)
{
    for (int servo = 0; servo < number_of_servos; servo++)
    {
        frames[servo] = data_to_use;
    }
}

int main()
{
    struct Header header;
    header.version = (uint8_t)CREATURE_VERSION;
    header.number_of_servos = (uint8_t)5;
    header.number_of_frames = (uint16_t)10;
    header.time_per_frame = (uint16_t)50;

    printf("The size of the header is: %ld\n", sizeof(header));

    FILE *sample_file = open_file(FILE_NAME, header);

    // Make a bunch of test animation frames
    for (int i = 0; i < header.number_of_frames; i++)
    {
        printf("writing frame %d\n", i);
        uint8_t data[header.number_of_servos];
        make_test_movement_frames(data, header.number_of_servos, i);
        write_movement_frame(sample_file, data, header.number_of_servos);
    }

    // Write out a pause frame
    //write_pause_frame(sample_file, (uint16_t)666);

    close_file(sample_file);

    return 0;
}
