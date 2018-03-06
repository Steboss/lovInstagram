#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False

import cython
import re,sys
cimport numpy as np

from libc.stdlib cimport malloc, free
from cpython.string cimport PyString_AsString

cdef extern from "c_code/markov.c":
    double probability_matrix(char **sentence, char **words, int lines_dim ,int words_dim)


cdef char ** to_cstring_array(list_str):
    cdef char **ret = <char **>malloc(len(list_str) * sizeof(char *))
    for i in xrange(len(list_str)):
        ret[i] = PyString_AsString(list_str[i])
    return ret


#first create a function which takes input the filename
#we cycle through it in order to find the single words
#we need cpdef to expose the function to python

cpdef double transition_matrix(filename) :
    #here we read the inputfile
    ifile = open(filename,"r")
    #create a list to store words
    words = []
    lines = []

    #here do in this way:
    #clean the sentence from all the punctuations
    #
    with ifile as reader:
        for line in reader:
            new_line = re.sub('[^A-Za-z0-9]+'," ", line)
            lines.append(new_line)
            #split
            splitter = new_line.split()
            for word in splitter:
                if word in words:
                    continue
                else:
                    words.append(word)
    #sanity check, do we have all the words in lines?
    #print(words)
    #print(lines)
    #print("Length of words %d\n" %len(words))
    #counter = 0
    #wordswords = []
    #for line in lines:
  #      splitter= line.split()
#        for split in splitter:#
#            if split in words:
#                if split in wordswords:
#                    continue
#                else :
#                    wordswords.append(split)
#                    counter+=1
#    print("Splitter in words %d\n"% counter)
#    sys.exit(-1)
    #now pass the list to the C code
    c_arr_dim = len(words)
    c_lines_dim = len(lines) #how many lines do we have?
    cdef char **c_arr = to_cstring_array(words)
    cdef char **c_line =to_cstring_array(lines)
    #pass to the c code also the filename, so we can read each line
    #take the c_arr dimensions to build a c_arr_dim*c_arr_dim matrix

    probability_matrix(c_line,c_arr,c_lines_dim,c_arr_dim)
