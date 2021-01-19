#!/usr/bin/make -f

CC=g++
CFLAGS=-I. -O2 -Wall
CXXFLAGS=-g -std=c++17 -Wall -pedantic

# Make everything by default
all: sample

creatures: creatures.cpp creatures.h
	$(CC) -c $(CFLAGS) creatures.cpp

sample: creatures sample.cpp
	$(CC) -o sample *.cpp $(CFLAGS)

# Don't run this on a make all
.PHONY: clean
clean:
	rm -f *.o *.bin sample