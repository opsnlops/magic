CC=gcc
CFLAGS=-I. -O2 -Wall

# Make everything by default
all: sample

creatures: creatures.c creatures.h
	$(CC) -c $(CFLAGS) creatures.c

sample: creatures sample.c
	$(CC) -o sample *.c $(CFLAGS)

# Don't run this on a make all
.PHONY: clean
clean:
	rm -f *.o *.bin sample