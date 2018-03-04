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
counter = 0
count_line = 0
with open("dataset.csv","r") as reader:
    for line in reader:
        count_line+=1
        #print(line)
        words = line.split()
        for word in words:
            pospos=0
            negneg=0
            wordswords = []
            classRes = classifier.classify(format_sentence(word))
            if classRes=="neg":
                neg +=1
                negneg+=1
            if classRes=="pos":
                pos +=1
                pospos+=1
            wordswords.append([words,classRes])
            counter+=1

#        if count_line<50:
 #           print(line)
 #           print("neg:%d pos:%d" %(negneg,pospos))
 #           print(wordswords)
 #           time.sleep(1)
print("Pos: %.4f" % (float(pos)/float(counter)))
print("Neg: %.4f" % (float(neg)/float(counter)))
