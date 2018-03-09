
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from nltk.metrics.scores import precision, recall
import sys
import nltk
import time
import math

def format_sentence(sent):
    return({word:True for word in  nltk.word_tokenize(sent)})

#prepare the positive comments
pos = []
reference = {}
reference["pos"]=[]
reference["neg"]=[]
testset={}
testset["pos"]=[]
testset["neg"]=[]

#these are 100 values
with open("basic_positive.csv","r") as reader:
    for line in reader:
        pos.append([format_sentence(line),"pos"])
        reference["pos"].append(line)

#negative comments
neg = []
with open("basic_negative.csv","r") as reader:
    for line in reader:
        neg.append([format_sentence(line),"neg"])
        reference["neg"].append(line)

#try to make a test  and training dataset
#for the training take the 50 percent of the comments
#then test with the reminiang 50 percent
#for the whole dataset take the whole pos and neg dataset and
#create the test set with the all dataset file

#Training part: last 50 elmeents
training = pos[:int((.5)*len(pos))] + neg[:int((.5)*len(neg))]
#this cryptic way to write it's just to select the last half part of the
#data set (above)
#
#test = pos[int((.5)*len(pos)):] + neg[int((.5)*len(neg)):]
#this will be the testdataset
#at the moment stick to the basic Bayes and train it
classifier = NaiveBayesClassifier.train(training)
print("Most informative features...")
print(classifier.show_most_informative_features())
#now try with the test dataset and assess the accuracy
for val in reference["pos"]:
    classRes = classifier.classify(format_sentence(val))
    if classRes=="pos":
        testset["pos"].append(val)
    else:
        testset["neg"].append(val)

for val in reference["neg"]:
    classRes=classifier.classify(format_sentence(val))
    if classRes=="pos":
        testset["pos"].append(val)
    else:
        testset["neg"].append(val)

true_pos = 0
false_pos = 0 #negaitve in realitiy, but positive in prediction
for val in testset["pos"]:
    if val in reference["pos"]:
        true_pos+=1
    else:
        false_pos+=1

print("True pos: %d" %true_pos)
true_neg = 0
false_neg = 0 #positive in reality, but negative prediction

for val in testset["neg"]:
    if val in reference["neg"]:
        true_neg+=1
    else:
        #the value is in reference["pos"]
        #so this is a positive evaluated negative, so its a false negative
        false_neg+=1
print("True pos: %d, false_pos:%d, true neg: %d, false neg:%d"% (true_pos, false_pos, true_neg, false_neg))
precision = true_pos/(true_pos+false_pos)
recall = true_pos/(true_pos+false_neg)
f1 = 2*((precision*recall)/(precision+recall))
print("Precision: %.2f" % precision)
print("Recall: %.2f" % recall)
print("F1: %.2f" % f1)
#compute the error
error = (false_pos + false_neg)/(false_pos + false_neg + true_pos + true_neg)
Ntot = (false_pos + false_neg + true_pos + true_neg)
ci = error + 1.96*math.sqrt(error*(1-error)/Ntot)
print("Error: %.2f" % ci)

sys.exit(-1)
#print(accuracy(classifier, test))

#now try to measure  the accuracy, the precision and recall
#create a dictionary to measure recall and precision

#pos = 0
#neg = 0
#counter = 0
#test_dataset = []
#with open("basic_positive.csv","r") as reader:
#    for line in reader:
#        test_dataset.append(line)
#        counter+=1
#        if counter==25:
#            break

#counter= 0
#with open("basic_negative.csv","r") as reader:#
#    for line in reader:
#        test_dataset.append(line)
#        counter+=1
#        if counter==25:
#            break
#for line in test_dataset:#
#    classRes = (classifier.classify(format_sentence(line)))
#    if classRes=="pos":
#        pos+=1
#    if classRes=="neg":
#        neg+=1

#print("Total pos %d  and neg %d out of 50\n" % (pos,neg))
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
