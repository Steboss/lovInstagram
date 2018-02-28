#script to collect all the important words from the total number of comment
#run in python3
import string

# load the document
filename = "3_clean.csv"
stopwords = []
with open("stopwords.csv","r") as reader:
    for line in reader:
        stopwords.append(line.strip())

tokens_list = []
#just for fun check which is the most used words
dict_words = {}

with open(filename,"r") as reader:
    for line in reader:
        tokens = line.split()
        #remove punctuations
        table_scheme = str.maketrans('','',string.punctuation)
        tokens = [w.translate(table_scheme) for w in tokens]
        #remove numbers?? for the momentskip it, since
        #there could be something like 4marzo
        #tokens= [word for word in tokens if word.isalpha()]
        #now filter out the stopwords
        tokens = [w for w in tokens if not w in stopwords]
        #filter all the words by length
        tokens = [word for word in tokens if len(word)>2]
        for token in tokens:
            if token in dict_words:
                dict_words[token]+=1
            else:
                dict_words[token]=1
            #remove the duplicates
            if token in tokens_list:
                continue
            else:
                tokens_list.append(token)

max_val = 0
values = []
for keys in dict_words.keys():
    values.append(dict_words[keys])


values.sort()
for i in range(len(values)-1,len(values)-50,-1):
    for keys in dict_words.keys():
        val = dict_words[keys]
        if val == values[i]:
            print(val, keys)
