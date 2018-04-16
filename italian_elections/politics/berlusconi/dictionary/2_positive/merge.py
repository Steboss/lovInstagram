words = []

with open("basic_positive.csv","r") as reader:
    for line in reader:
        words.append(line)

with open("positive_reference.csv","r") as reader:
    for line in reader:
        if line in words:
            continue
        else:        
            words.append(line)



words.sort()
#write everything 
ofile = open("positive.csv","w")

for word in words:
    ofile.write(word)
