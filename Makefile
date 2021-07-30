all:
	gcc -O3 -Wall -pthread -o 38khz 38khz.c -lpigpiod_if2 -lrt
