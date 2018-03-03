#script to retrieve the most profile with the high number of followers
#and their caption, to see if they are significant
#usually very famous profile do not share menaingful information

import pandas as pd
import numpy as np
import sys
df = pd.read_csv("1_clean.csv",names=["username","followers","following","caption","likes","comments","day","month","year","hour","min","s"])

df = df.loc[df["followers"]<50000]
#print(len(df))
df.to_csv("2_clean.csv",index=False,header=False)
