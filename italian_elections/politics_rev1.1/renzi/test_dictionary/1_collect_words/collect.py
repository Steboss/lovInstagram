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

print("Most recurring words...")
#this is just to have fun
max_val = 0
values = []
for keys in dict_words.keys():
    values.append(dict_words[keys])

values.sort()
for i in range(len(values)-1,len(values)-100,-1):
    for keys in dict_words.keys():
        if len(keys)>5:
            val = dict_words[keys]
            if val == values[i]:
                print(val, keys)

#now save all the words in a filename
#reduce the dictionary dimensions, the token
#must have a value > 5

all_words = []
print("Generation of a raw list of words...")
ofile = open("raw_list_words.csv","w")
for keys in dict_words.keys():
    if len(keys)>4:
        if dict_words[keys]>5:
            all_words.append(keys)

all_words.sort()

for word in all_words:
    ofile.write("%s\n" % word)
ofile.close()
