#!/usr/bin/env python3

# This file smooths data that came off the senors to something
# that looks less jaggy

import csv

from scipy.signal import savgol_filter

servo_lower_bound = 0
servo_upper_bound = 179

data_file = 'data/sample_raw.csv'

raw_data = []

def remove_comments(csvfile):
    for row in csvfile:
        raw = row.split('#')[0].strip()
        if raw: yield row

def smooth_data(raw_data, window_length=None, polyorder=None):
    window_length = window_length or 11
    polyorder = polyorder or 3

    finished_data = []

    smoothed_data = savgol_filter(raw_data, window_length, polyorder)
    for point in smoothed_data:

        # Make sure we're in range of the servo
        int_point = round(point)

        if int_point < servo_lower_bound:
            int_point = servo_lower_bound
        elif int_point > servo_upper_bound:
            int_point = servo_upper_bound

        finished_data.append(int_point)
    
    return finished_data

with open(data_file) as raw:
    csv_reader = csv.reader(remove_comments(raw))

    for row in csv_reader:
        raw_data.append(int(row[0]))

print(raw_data)

smoothed_data = smooth_data(raw_data)

for point in smoothed_data:
    print(point)
