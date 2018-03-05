
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
import sys
import nltk
import time

def format_sentence(sent):
    return({word:True for word in  nltk.word_tokenize(sent)})

#prepare the positive comments
pos = []
with open("basic_positive.csv","r") as reader:
    for line in reader:
        pos.append([format_sentence(line),"pos"])
#negative comments
neg = []
with open("basic_negative.csv","r") as reader:
    for line in reader:
        neg.append([format_sentence(line),"neg"])

#try to make a test  and training dataset
#for the training take the 50 percent of the comments
#then test with the reminiang 50 percent
#for the whole dataset take the whole pos and neg dataset and
#create the test set with the all dataset file

#Training part
training = pos[:int((.5)*len(pos))] + neg[:int((.5)*len(neg))]
#this cryptic way to write it's just to select the last half part of the
#data set (above)
#and the first half dataset (below)
test = pos[int((.5)*len(pos)):] + neg[int((.5)*len(neg)):]
counter = 0
test_dataset = []
with open("basic_positive.csv","r") as reader:
    for line in reader:
        test_dataset.append(line)
        counter+=1
        if counter==25:
            break

print(len(test_dataset))
counter= 0
with open("basic_negative.csv","r") as reader:
    for line in reader:
        test_dataset.append(line)
        counter+=1
        if counter==25:
            break
print(len(test_dataset))
#this will be the testdataset


#at the moment stick to the basic Bayes
classifier = NaiveBayesClassifier.train(training)
print("Most informative features...")
print(classifier.show_most_informative_features())
#now try with the test dataset and assess the accuracy
print(accuracy(classifier, test))

pos = 0
neg = 0
for line in test_dataset:

    classRes = (classifier.classify(format_sentence(line)))
    if classRes=="pos":
        pos+=1
    if classRes=="neg":
        neg+=1

print("Total pos %d  and neg %d out of 50\n" % (pos,neg))
#now if the result is good enough, let's process the real dataset
pos_line = 0
neg_line = 0
counter_line = 0
with open("dataset.csv","r") as reader:
    for line in reader:
        counter_line+=1
        classRes = classifier.classify(format_sentence(line))
        if classRes =="pos":
            pos_line+=1
        if classRes =="neg":
            neg_line+=1
print("Total pos %d and neg %d out of total comments %d\n" %(pos_line,neg_line,counter_line))
print("Percentage: pos %.2f  and neg %.2f " % ((pos_line/counter_line), (neg_line/counter_line)) )
