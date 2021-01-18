#!/usr/bin/env python3

# This file smooths data that came off the senors to something
# that looks less jaggy

import csv

data_file = 'data/sample_raw.csv'

with open(data_file) as raw:
    csv_reader = csv.reader(raw)

    for row in csv_reader:
        print(row)
