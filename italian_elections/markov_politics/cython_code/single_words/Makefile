all:
	cython markov.pyx
	gcc -g -O3 -fpic -c markov.c `python-config --cflags`  -std=c99
	gcc markov.o -o markov.so -shared `python-config --ldflags` -std=c99
