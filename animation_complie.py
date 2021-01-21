#!/usr/bin/env python3

import csv
from os import stat_result
import struct


"""
struct Header
{
    uint8_t version;
    uint8_t number_of_servos;
    uint16_t number_of_frames;
    uint16_t time_per_frame; // Number of milliseconds for each frame
} __attribute__((packed));
"""


magic_number = b"RAWR!"
version = 1


data_file = "data/smoothed_data.csv"

raw_data = []


def make_header(number_of_servos, number_of_frames, time_per_frame):
    return magic_number + struct.pack(
        "BBHH",
        version,
        number_of_servos,
        number_of_frames,
        time_per_frame,
    )


def make_frame(servos, number_of_servos):

    # Make sure we've got the right number of servos
    if len(servos) != number_of_servos:
        print(f"Number of servos in this frame wasn't {number_of_servos}!")

    bytes = struct.pack("B", 1)

    for servo in servos:
        bytes += struct.pack("B", int(servo))

    return bytes


def remove_comments(csvfile):
    for row in csvfile:
        raw = row.split("#")[0].strip()
        if raw:
            yield row


with open(data_file) as raw:
    csv_reader = csv.reader(remove_comments(raw))

    for row in csv_reader:
        raw_data.append(row)

number_of_frames = len(raw_data)
print(f"there are {number_of_frames} frames")

number_of_servos = len(raw_data[0])
print(f"assuming {number_of_servos} servo(s) per frame")


with open("sample.bin", "wb") as output:

    output.write(make_header(number_of_servos, number_of_frames, 50))

    for frame in raw_data:
        output.write(make_frame(frame, number_of_servos))
