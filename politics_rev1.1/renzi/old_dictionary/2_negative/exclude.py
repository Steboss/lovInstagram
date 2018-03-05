pos = []
with open("basic_positive.csv","r") as reader:
    for line in reader:
        pos.append(line)

all_words = []
with open("raw_list_words.csv","r") as reader:
    for line in reader:
        all_words.append(line)

excluded = []

for words in all_words:
    if words in pos:
        continue
    else:
        excluded.append(words)

ofile = open("basic_negative.csv","w")

for words in excluded:
    ofile.write(words)        
