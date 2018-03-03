pos = []

with open("basic_positive.csv","r") as reader:
    for line in reader:
        pos.append(line)

neg = []

with open("basic_negative.csv","r") as reader:
    for line in reader:
        neg.append(line)

ofile = open("basic_neutral.csv","w")

all = pos + neg

with open("raw_list_words.csv","r") as reader:
    for line in reader:
        if line in all:
            continue
        else:
            ofile.write(line)
