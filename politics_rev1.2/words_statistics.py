import os,sys
import numpy as np
import math

def store_list(filename):

    current_list =[]
    with open(filename,"r") as reader:
        for line in reader:
            current_list.append(line)
    return current_list

def average_length(comm_list):
    #here we need to count the character
    val_list = []
    for line in comm_list:
        counter = 0
        for character in line:
            counter+=1
        val_list.append(counter)
    #compute the averageand std dev
    mean = np.mean(val_list)
    #1 sigma only
    stddev = np.std(val_list)/math.sqrt(len(val_list))
    return mean,stddev

def average_words(comm_list):
    #here we are computing the average number of words in each comment

    val_list = []
    for line in comm_list:
        words = line.split()
        val_list.append(len(words))
    #compute the averageand std dev
    mean = np.mean(val_list)
    #1 sigma only
    stddev = np.std(val_list)/math.sqrt(len(val_list))
    return mean,stddev

def most_repeated(comm_list):

    dict_val = {}
    for line in comm_list:
        words = line.split()
        for word in words:
            if len(word)>=6:
                if word in dict_val:
                    dict_val[word]+=1
                else:
                    dict_val[word] = 1

    values = []
    for words in dict_val.keys():
        values.append(dict_val[words])
    #sort
    values.sort()
    #print(values)

    for i in range(len(values)-1,len(values)-51,-1):
        for words in dict_val.keys():
            if dict_val[words]== values[i]:
                print(values[i],words)


berlusconi = store_list("berlusconi.csv")
dimaio     = store_list("dimaio.csv")
renzi = store_list("renzi.csv")
salvini = store_list("salvini.csv")

#find the length of each comment
berl_avg, berl_std = average_length(berlusconi)
di_avg, di_std = average_length(dimaio)
re_avg, re_std = average_length(renzi)
sa_avg, sa_std = average_length(salvini)
print("Average character length:")
print("Berlusconi\t\t%.2f+/-%.2f" % (berl_avg,berl_std))
print("DiMaio\t\t%.2f+/-%.2f" % (di_avg,di_std))
print("Renzi\t\t%.2f+/-%.2f" % (re_avg,re_std))
print("Salvini\t\t%.2f+/-%.2f" % (sa_avg,sa_std))


berl_avg, berl_std = average_words(berlusconi)
di_avg, di_std = average_words(dimaio)
re_avg, re_std = average_words(renzi)
sa_avg, sa_std = average_words(salvini)
print("Average comments words length:")
print("Berlusconi\t\t%.2f+/-%.2f" % (berl_avg,berl_std))
print("DiMaio\t\t%.2f+/-%.2f" % (di_avg,di_std))
print("Renzi\t\t%.2f+/-%.2f" % (re_avg,re_std))
print("Salvini\t\t%.2f+/-%.2f" % (sa_avg,sa_std))

#find the most repeatedwords for each candidate
#here we need a histogram
print("Berlusconi")
most_repeated(berlusconi)
print("Dimaio")
most_repeated(dimaio)
print("Re")
most_repeated(renzi)
print("Sa")
most_repeated(salvini)
