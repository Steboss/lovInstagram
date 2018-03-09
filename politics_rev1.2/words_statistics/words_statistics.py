import os,sys
import numpy as np
import math
import string

#run with python3!
def store_list(filename):

    current_list =[]
    words = []  #list of single words --cleaned by punctuations
    with open(filename,"r") as reader:
        for line in reader:
            current_list.append(line)

    with open(filename,"r") as reader:
        for line in reader:
            splitter = line.split()
            for split in splitter:
                #these are the single words, clean them and make loweracse
                translator = str.maketrans('','',string.punctuation)
                word_clean = split.translate(translator)
                word_clean = word_clean.lower()
                if word_clean in words:
                    continue
                else:
                    words.append(word_clean)

    return current_list, words

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

def most_repeated(comm_list,filename):
    ofile = open(filename,"w")

    dict_val = {}
    tot_words = 0
    for line in comm_list:
        words = line.split()
        for word in words:
            if len(word)>=6:
                if word in dict_val:
                    dict_val[word]+=1
                else:
                    dict_val[word] = 1
                tot_words+=1

    values = []
    for words in dict_val.keys():
        values.append(dict_val[words])
    #sort
    values.sort()
    #print(values)
    repeated = []
    for i in range(len(values)-1,len(values)-51,-1):
        for words in dict_val.keys():
            if dict_val[words]== values[i]:
                print(values[i],words)
                ofile.write("%.2f, %s\n"% ((values[i]/tot_words),words))

def uniquewords(words1,label1,words2,label2,words3,label3,words4,label4):
    #very bad function, try to optimize it
    uniques={}
    uniques[label1]=[]
    uniques[label2]=[]
    uniques[label3]=[]
    uniques[label4]=[]
    print("Dictionary 1...")

    for word in words1:
        if len(word)< 3:
            continue
        else:
            if (word in words2) or (word in words3) or (word in words4):
                try:
                    del words1[words1.index(word)]
                except:
                    pass
                try:
                    del words2[words2.index(word)]
                except:
                    pass
                try:
                    del words3[words3.index(word)]
                except:
                    pass
                try:
                    del words4[words4.index(word)]
                except:
                    pass
            else:
                uniques[label1].append(word)

    print("Dictionary 2...")
    for word in words2:
        if len(word)< 3:
            continue
        else:
            if (word in words1) or (word in words3) or (word in words4):
                try:
                    del words1[words1.index(word)]
                except:
                    pass
                try:
                    del words2[words2.index(word)]
                except:
                    pass
                try:
                    del words3[words3.index(word)]
                except:
                    pass
                try:
                    del words4[words4.index(word)]
                except:
                    pass
            else:
                uniques[label2].append(word)

    print("Dictionary 3...")
    for word in words3:
        if len(word)< 3:
            continue
        else:
            if (word in words1) or (word in words2) or (word in words4):
                try:
                    del words1[words1.index(word)]
                except:
                    pass
                try:
                    del words2[words2.index(word)]
                except:
                    pass
                try:
                    del words3[words3.index(word)]
                except:
                    pass
                try:
                    del words4[words4.index(word)]
                except:
                    pass
            else:
                uniques[label3].append(word)
    print("Dictionary 4...")
    for word in words4:
        if len(word)< 3:
            continue
        else:
            if (word in words1) or (word in words2) or (word in words3):
                try:
                    del words1[words1.index(word)]
                except:
                    pass
                try:
                    del words2[words2.index(word)]
                except:
                    pass
                try:
                    del words3[words3.index(word)]
                except:
                    pass
                try:
                    del words4[words4.index(word)]
                except:
                    pass
            else:
                uniques[label4].append(word)

    return uniques

#MAIN#
berlusconi,berlusconi_words = store_list("berlusconi.csv")
dimaio,dimaio_words     = store_list("dimaio.csv")
renzi,renzi_words = store_list("renzi.csv")
salvini,salvini_words = store_list("salvini.csv")

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
os.makedirs("repeated_words")

most_repeated(berlusconi,"repeated_words/berlusconi.dat")

most_repeated(dimaio,"repeated_words/dimaio.dat")

most_repeated(renzi,"repeated_words/renzi.dat")

most_repeated(salvini,"repeated_words/salvini.dat")

sys.exit(-1)
dict_res =uniquewords(berlusconi_words,"berlusconi",dimaio_words,"dimaio",\
                      salvini_words,"salvini",renzi_words,"renzi")

os.makedirs("unique_words")
ofberlu = open("unique_words/berlusconi_uniq.dat","w")
ofdimaio = open("unique_words/dimaio_uniq.dat","w")
ofrenzi = open("unique_words/renzi_uniq.dat","w")
ofsalvi = open("unique_words/salvini_uniq.dat","w")

print("Writing files of uniques words...")

vals = []
for values in dict_res["berlusconi"]:
    vals.append(values)
vals.sort()
for val in vals:
    ofberlu.write("%s\n"% val)

vals = []
for values in dict_res["salvini"]:
    vals.append(values)
vals.sort()
for val in vals:
    ofsalvi.write("%s\n"% val)

vals = []
for values in dict_res["dimaio"]:
    vals.append(values)
vals.sort()
for val in vals:
    ofdimaio.write("%s\n"% val)

vals = []
for values in dict_res["renzi"]:
    vals.append(values)
vals.sort()
for val in vals:
    ofrenzi.write("%s\n"%val)

ofberlu.close()
ofsalvi.close()
ofdimaio.close()
ofrenzi.close()
