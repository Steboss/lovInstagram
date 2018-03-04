import json
import requests
import time
import bs4 as bs
import contextlib
import urllib
import os,sys,datetime, random,re, argparse
import sqlite3


def open_database(database):


    try:
        conn = sqlite3.connect(database)
        conn.text_factory  =str
    except sqlite3.Error as e:
        print(e)
        sys.exit(-1)
    return conn


def remove_users(database,users):

    #use the cursor
    cursor = database.cursor()
    for user in users:
        take_out_command = cursor.execute('''DELETE FROM politics WHERE  username="%s"; ''' % user)
        print(take_out_command)
        database.commit()


#read the usernames to take out
ifile = open("usernames.dat","r")
#read the database
database = sys.argv[1]
#open the database
connection = open_database(database)
#collect users
users = []
print("Collecting users...")
with ifile as reader:
    for line in reader:
        users.append(line.strip())
print(users)
print("Removing users...")
remove_users(connection,users)
