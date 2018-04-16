ifile = open("basic_negative.csv","r")
negs = []
with ifile as reader:
    for line in reader:
        negs.append(line.strip())
negs.sort()
ofile = open("new_neg.csv","w")
for neg in negs:
    ofile.write("%s\n"%neg)

poss = []
with open("basic_positive.csv","r") as reader:
    for line in reader:
        poss.append(line.strip())

ofile.close()
ofile = open("new_pos.csv","w")
for pos in poss:
    ofile.write("%s\n"%pos)
