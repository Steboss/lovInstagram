import re
ofile = open("2_clean.csv","w")
with open("clean.csv","r") as reader:
   for line in reader:
       line = line.replace('"','')
       #remove blank lines
       if re.match(r"^\s*$", line):
           continue
       else:
           ofile.write(line)       
             
