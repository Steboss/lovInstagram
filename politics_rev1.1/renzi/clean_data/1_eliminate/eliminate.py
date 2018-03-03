import pandas as pd
import sys

df = pd.read_csv(sys.argv[1],names=["comment_text"])

#remove all the tagged user, along with the hashtag symbol and quotes
df["comment_text"]=df["comment_text"].replace({"(@\w+)":""},regex=True)
#replace also the @ symbol
df["comment_text"]=df["comment_text"].replace({"@":""},regex=True)
df["comment_text"]=df["comment_text"].replace({"#":""},regex=True)
df["comment_text"]=df["comment_text"].replace({'\"':" "})
df['comment_text'] = df["comment_text"].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))

df.to_csv("clean.csv",index=False,header=False)
