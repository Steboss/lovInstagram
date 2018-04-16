#cython: boundscheck=False
#cython: wraparound=False
#cython: nonecheck=False

import re,sys
cimport numpy as np
cimport cython
from cpython cimport array

from libc.stdlib cimport malloc, free
from cpython.string cimport PyString_AsString

cdef extern from "c_code/markov.c":
  double** probability_matrix(char **sentences,char **words, int lines_dim ,int words_dim)

cdef char ** to_cstring_array(list_str):
    cdef char **ret = <char **>malloc(len(list_str) * sizeof(char *))
    for i in xrange(len(list_str)):
        ret[i] = PyString_AsString(list_str[i])
    return ret


#first create a function which takes input the filename
#we cycle through it in order to find the single words
#we need cpdef to expose the function to python

cdef double** transition_matrix(filename) :
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
            #lowercase
            new_line = new_line.lower()
            lines.append(new_line)
            if re.match(r'^\s*$', new_line):
                continue #white line
            else:
                #split
                splitter = new_line.split()
                for word in splitter:
                    if word in words:
                        continue
                    else:
                        words.append(word.lower())

    #TODO ADD ASANITY CHECK between words andlines
    #now pass the list to the C code
    c_arr_dim = int(len(words))
    c_lines_dim = int(len(lines)) #how many lines do we have?
    #sort in alphabetical order the words? but this would require then to look for the words
    cdef char **c_arr = to_cstring_array(words)
    cdef char **c_line =to_cstring_array(lines)
    #pass to the c code also the filename, so we can read each line
    #take the c_arr dimensions to build a c_arr_dim*c_arr_dim matrix
    #define a double pointer /memory view element
    cdef double **mat_pointer
    mat_pointer = <double **> malloc((c_arr_dim)*cython.sizeof(double))

    mat_pointer = probability_matrix(c_line,c_arr,(c_lines_dim),(c_arr_dim))
    #converting the double** pointer to a numpy array
    #mat_view = np.PyArray_SimpleNewFromData(2,[c_arr_dim,c_arr_dim],np.NPY_FLOAT64,mat_pointer)
    #here we can have the transition matrix

    for i in range(c_arr_dim):
        for j in range(c_arr_dim):
            if mat_pointer[i][j]>0.0:
              print("words %s and %s  prob %.4f" % (words[i],words[j],mat_pointer[i][j]))



cpdef main_work(filename):
    transition_matrix(filename)
