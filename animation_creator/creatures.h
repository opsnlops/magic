
#ifndef _APRILS_CREATURES_WAS_HERE
#define _APRILS_CREATURES_WAS_HERE

#include <stdint.h>
#include <array>
#include <list>

#define CREATURE_VERSION 1

#define MOVEMENT_FRAME_TYPE 1
#define PAUSE_FRAME_TYPE 2
#define LED_CONTROL_FRAME_TYPE 3

#define MAGIC_NUMBER "RAWR"

using byte = unsigned char;

class Header
{
public:
    uint8_t version;
    uint8_t number_of_servos;
    uint16_t number_of_frames;
    uint16_t time_per_frame;

    Header();
    Header(uint8_t _number_of_servos, uint16_t _number_of_frames, uint16_t _time_per_frame);

    template <typename T>
    std::array<byte, sizeof(T)> to_bytes();
};

class Frame
{
public:
    uint8_t type;
    std::list<uint8_t> data;
};

Frame make_movement_frame(uint8_t *servo_values);

#endif
