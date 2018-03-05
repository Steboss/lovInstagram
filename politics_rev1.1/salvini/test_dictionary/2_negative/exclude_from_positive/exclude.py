#exclude all the words present in basic_positive from teh raw list

pos_words = []

with open("basic_positive.csv","r") as reader:
    for line in reader:
        pos_words.append(line.strip())

all_words = []

with open("raw_list_words.csv","r") as reader:
    for line in reader:
        if line in pos_words:
            continue
        else:
            all_words.append(line.strip())


all_words.sort()
ofile = open("raw_negative.csv","w")
for word in all_words:
    if word in pos_words:
        continue
    else:
        ofile.write("%s\n" % word)
