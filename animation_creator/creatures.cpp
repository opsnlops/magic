
#include <array>
#include <memory>
#include <type_traits>
#include <iostream>
#include <iomanip>
#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "creatures.h"

Header::Header()
{
    printf("Hi I'm a header\n");
    version = (uint8_t)CREATURE_VERSION;
}

Header::Header(uint8_t _number_of_servos, uint16_t _number_of_frames, uint16_t _time_per_frame)
{
    printf("Hi I'm also a header\n");
    version = (uint8_t)CREATURE_VERSION;
    number_of_servos = _number_of_servos;
    number_of_frames = _number_of_frames;
    time_per_frame = _time_per_frame;
}

template <typename T>
std::array<byte, sizeof(T)> Header::to_bytes()
{
    printf("serializing to a pointer");

    std::list<byte, sizeof(T)> bytes;

    bytes.

    const byte *begin = reinterpret_cast<const byte *>(std::addressof(data));
    const byte *end = begin + sizeof(T);
    std::copy(begin, end, std::begin(bytes));

    return bytes;
}

Frame make_movement_frame(std::list<uint8_t> servo_values)
{
    Frame frame;
    frame.type = (uint8_t)MOVEMENT_FRAME_TYPE;
    frame.data = servo_values;

    return frame;
}