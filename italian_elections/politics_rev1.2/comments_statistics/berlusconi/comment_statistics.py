#Here we are going to retrieve the average of comments for each post o
#the average number of likes for each post o
#the total number of likes     O
#the total number of comments O
#the least liked picture o
#the most liked picture o
import os,sys
import numpy as np
import scipy
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sbn
sbn.set_style("whitegrid")

#input : a name for the database,  a name ofr the outpufile to write all the info
#the csv file with the n_likes, n_comments, shortcode
def open_database(database):


    try:
        conn = sqlite3.connect(database)
        conn.text_factory  =str
    except sqlite3.Error as e:
        print(e)
        sys.exit(-1)
    return conn

def total_comments(database,ofile):
    #here we are going to extract ht etotal number of comments and write to file ofile
    cursor = database.cursor()
    #thte total number of comments is the total number of rowas
    command = cursor.execute('''SELECT count(*) FROM politics;''')
    
    for comm in command:
        tot_com = comm[0]

    ofile.write("Total number of comments: %d\n" % tot_com)

def total_likes(csvfile,ofile):
    #here we are selecting the total number of likes
    #cursor = database.cursor()
    #command = cursor.execute('''SELECT DISTINCT n_likes FROM politics;''')
    #likes = 0
    #for comm in command:
#        likes+=comm[0]
#    ofile.write("Total number of likes %d\n" % likes)
    #compute the total number of likes
    tot_likes = 0
    tmp = 0
    with open(csvfile,"r") as reader:
        for line in reader:
            shortcode = line.split(",")[2]
            likes = int(line.split(",")[0])
            if tmp==shortcode:
                continue
            else:
                tot_likes+=likes
                tmp = shortcode

    ofile.write("Total number of likes %d\n"% tot_likes)

def average(csvfile,ofile):
    #compute the average number of comments
    #compute the average number of likes
    #and detect the photo with more likes and with least likes
    #and detect the photo with more comment sand least comments
    photos = {}
    comm_list = []
    like_list = []
    tmp = 0
    with open(csvfile,"r") as reader:
        for line in reader:
            shortcode = line.split(",")[2]
            likes = int(line.split(",")[0])
            comments = int(line.split(",")[1])
            if tmp==shortcode:
                #here we are on the same photo , skip it
                continue
            else:
                like_list.append(likes)
                comm_list.append(comments)
                photos[shortcode]=[likes,comments]
                tmp = shortcode

    #compute the averages
    avg_comm = np.mean(comm_list)
    std_comm = np.std(comm_list)
    avg_like = np.mean(like_list)
    std_like = np.std(like_list)
    #now detect the photo with more likes
    max_likes = 0
    max_comments =0

    counter_likes = 0
    counter_comments = 0

    for key in photos.keys():
        likes = photos[key][0]
        comments = photos[key][1]
        shortcode = key
        #max likes
        if likes> max_likes:
            max_likes = likes
            max_liked_photo = shortcode
        else:
            if counter_likes==0:
                min_likes = likes
                counter_likes+=1
            else:
                if likes< min_likes:
                    min_likes=likes
                    least_liked_photo = shortcode

        if comments>max_comments:
            max_comments= comments
            max_commented_photo = shortcode
        else:
            if counter_comments ==0:
                min_comments = comments
                counter_comments +=1
            else:
                if comments< min_comments:
                    min_comments = comments
                    least_commented_photo = shortcode




    print("Average number of comments per post  %.2f +/- %.2f" % (avg_comm,std_comm))
    ofile.write("Average number of comments per post  %.2f +/- %.2f\n" % (avg_comm,std_comm))
    print("Average number of likes per post %.2f +/- %.2f" %(avg_like,std_like))
    ofile.write("Average number of likes per post %.2f +/- %.2f\n" %(avg_like,std_like))
    #it's interesting here to compute hte  number of likes every 20 posts
    for i in range(0, len(like_list),20):
        batch = like_list[i:i+19]
        avg_batch = np.mean(batch)
        ofile.write("Average of likes for posts within %d    %d  : %.2f\n" % (i,i+19,avg_batch))

    print("Maximum number of likes %d for the photo %s" % (max_likes, max_liked_photo))
    ofile.write("Maximum number of likes %d for the photo https://www.instagram.com/p/%s/ \n" % (max_likes, max_liked_photo))
    print("Minimum number of likes %d for the photo %s" % (min_likes, least_liked_photo))
    ofile.write("Minimum number of likes %d for the photo https://www.instagram.com/p/%s/ \n" % (min_likes, least_liked_photo))
    print("Maximum number of comments %d for the photo %s" % (max_comments, max_commented_photo))
    ofile.write("Maximum number of comments %d for the photo https://www.instagram.com/p/%s/ \n" % (max_comments, max_commented_photo))
    print("Minimum number of comments %d for the photo %s" % (min_comments, least_commented_photo))
    ofile.write("Minimum number of comments %d for the photo https://www.instagram.com/p/%s/ \n" % (min_comments, least_commented_photo))

    #create a timeseries behaviour
    fig,ax = plt.subplots(figsize=(10,10))
    color= sbn.color_palette()
    marker = "o"
    x_linspace = np.linspace(0,len(comm_list),len(comm_list))

    ax.plot(x_linspace, comm_list, color=color[0], marker=marker)
    ax.xaxis.set_tick_params(labelsize=18)
    ax.yaxis.set_tick_params(labelsize=18)
    ax.set_ylabel(r"n$^\circ$ comments",fontsize=18)
    ax.set_xlabel(r"n$^\circ$ post",fontsize=18)
    ax.set_xlim(0,len(comm_list))
    fig.tight_layout()
    plt.savefig("comments.pdf")
    #likes + interpolation
    fig,ax = plt.subplots(figsize=(10,10))
    color= sbn.color_palette()
    marker = "o"
    x_linspace = np.linspace(0,len(like_list),len(like_list))
    #interpol_equation = scipy.interpolate.interp1d(x_linspace,like_list,kind="linear")
    #interpolation_line = interpol_equation(x_linspace)
    ax.plot(x_linspace, like_list, color=color[1], marker=marker)
    #ax.plot(x_linspace, interpolation_line,color=color[2],marker="+")
    ax.xaxis.set_tick_params(labelsize=18)
    ax.yaxis.set_tick_params(labelsize=18)
    ax.set_ylabel(r"n$^\circ$ likes",fontsize=20)
    ax.set_xlabel(r"n$^\circ$ post",fontsize=20)
    ax.set_xlim(0,len(like_list))
    fig.tight_layout()
    plt.savefig("likes.pdf")
    plt.savefig("likes.png",dpi=300,transparent=True)





#MAIN
databasename =  sys.argv[1]
ofile  = open(sys.argv[2],"w")
csvfile = (sys.argv[3])
#open the database

database = open_database(databasename)
#now we need to compute the total number of likes
#and the totalnumber of comments
print("total number of comments")
total_comments(database, ofile)
#now the sum of the total likes
print("total number of likes")
total_likes(csvfile,ofile)
average(csvfile,ofile)
