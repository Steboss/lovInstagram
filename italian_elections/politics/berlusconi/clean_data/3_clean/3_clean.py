#here I am remove a comment which is meaningless:
#votodroghiere
#gino --> damn youtubers!
ofile = open("3_clean.csv","w")
samples = 0 
with open("2_clean.csv","r") as reader:
    for line in reader:
        if "votodroghiere" in line:
            continue
        elif "votadroghiere" in line:
            continue
        elif "droghiere" in line:
            continue
        elif "gino" in line:
            continue
        else:
            ofile.write(line)
            samples+=1

print("Total number of entries %d" % samples)
