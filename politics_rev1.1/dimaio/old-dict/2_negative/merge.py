words = []

with open("basic_negative.csv","r") as reader:
    for line in reader:
        words.append(line)

with open("negative_reference.csv","r") as reader:
    for line in reader:
        if line in words:
            continue
        else:        
            words.append(line)



words.sort()
#write everything 
ofile = open("negative.csv","w")

for word in words:
    ofile.write(word)
