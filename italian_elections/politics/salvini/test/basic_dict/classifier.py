from nltk.classify import NaiveBayesClassifier
import sys
import nltk

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
neut = []
with open("basic_neutral.csv","r") as reader:
    for line in reader:
        neut.append(line)


positive_feature = [ (format_sentence(pos_term),"pos") for pos_term in pos]
negative_feature = [ (format_sentence(neg_term),"neg") for neg_term in neg]
neutral_feature  = [ (format_sentence(neut_term),"neut") for neut_term in neut]

train_test = positive_feature + negative_feature  + neutral_feature
classifier = NaiveBayesClassifier.train(train_test)

pos = 0
neut = 0 
neg = 0
counter = 0 
with open("dataset.csv","r") as reader:
    for line in reader:
        words = line.split()
        for word in words:
            classRes = classifier.classify(format_sentence(word))
            if classRes=="neg":
                neg +=1
            if classRes=="pos":
                pos +=1
            if classRes =="neut":
                neut+=1
            counter+=1

print("Pos: %.4f" % (float(pos)/float(counter)))
print("Neg: %.4f" % (float(neg)/float(counter)))       
print("Neut:%.4f" % (float(neut)/float(counter)))
