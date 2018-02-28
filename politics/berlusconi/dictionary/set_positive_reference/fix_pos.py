import sys

ofile = open("positive_reference.csv","w")
pos = []
with open(sys.argv[1],"r") as reader:
    for line in reader:
        pos.append(line.strip())

pos.sort()

#remove thedouble entities
clean = []
for entities in pos:
    if entities in clean:
        continue
    elif "y" in entities:
        continue #this is an English item
    else:
        clean.append(entities)

for entities in clean:
    ofile.write("%s\n" % (entities))         
