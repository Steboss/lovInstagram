
from nltk.classify import NaiveBayesClassifier
import sys
import nltk
import time
def format_sentence(sent):
    return({word:True for word in  nltk.word_tokenize(sent)})



pos = []

with open("basic_positive.csv","r") as reader:
    for line in reader:
        pos.append(line)
neg = []
with open("basic_negative.csv","r") as reader:
    for line in reader:
        neg.append(line)


positive_feature = [ (format_sentence(pos_term),"pos") for pos_term in pos]
negative_feature = [ (format_sentence(neg_term),"neg") for neg_term in neg]

train_test = positive_feature + negative_feature
classifier = NaiveBayesClassifier.train(train_test)

pos = 0
neg = 0
pos_line = 0
neg_line = 0
counter = 0
count_line = 0
#try to save the pos and neg comments
#this can be helpful to perform a further machine learning test
pos_file = open("positive_comments.csv","w")
neg_file = open("negative_comments.csv","w")

with open("dataset.csv","r") as reader:
    for line in reader:
        count_line+=1 #this is the single comment
        #print(line)
        words = line.split()
        for word in words:
            pospos=0
            negneg=0
            #wordswords = []
            classRes = classifier.classify(format_sentence(word))
            if classRes=="neg":
                neg +=1
                negneg+=1
            if classRes=="pos":
                pos +=1
                pospos+=1
        #check which are the positive comments
        if pospos> negneg:
            pos_line+=1
            pos_file.write(line)
        else:
            neg_line+=1
            neg_file.write( line)

        #if count_line<50:
        #    print(line)
        #    print("neg:%d pos:%d" %(negneg,pospos))
            #print(wordswords)
        #    time.sleep(1)

pos_file.close()
neg_file.close()
print("Pos raw %d out of %d" % (pos_line,count_line))
print("Neg raw %d out of %d" % (neg_line,count_line))

#print("Pos: %.4f" % (float(pos)/float(counter)))
#print("Neg: %.4f" % (float(neg)/float(counter)))
