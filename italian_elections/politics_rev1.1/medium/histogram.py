import matplotlib.pyplot as plt
from numpy import *
import math, os, sys, re
import seaborn as sbn
sbn.set_style("whitegrid")

#select seaborn color palette to color all the bars
colors =sbn.color_palette()
ind = arange(4) - 0.25 #add a -0.25 so we center the plot
#width of each bar
width = 0.25 #which is the same as the spacing
fig = plt.figure(figsize=[10,7])
ax = fig.add_subplot(111)

#BARS:
berlusconi = [0.43,0.57]
berlusconi_err = [0.13,0.13]
salvini = [0.46, 0.54]
salvini_err = [0.18,0.18]
renzi = [0.14,0.86]
renzi_err = [0.11,0.11]
dimaio = [0.68,0.32]
dimaio_err = [0.19,0.19]

berluP =ax.bar(ind[0],berlusconi[0],width,color=colors[0],yerr=berlusconi_err[0],\
            error_kw = dict(elinewidth=2,ecolor="black")   )
berluN = ax.bar(ind[0]+width,berlusconi[1],width,color=colors[2],yerr=berlusconi_err[0],\
            error_kw = dict(elinewidth=2,ecolor="black")   )

ax.bar(ind[1],salvini[0],width,color=colors[0],yerr=salvini_err[0],\
            error_kw = dict(elinewidth=2,ecolor="black")   )
ax.bar(ind[1]+width,salvini[1],width,color=colors[2],yerr=salvini_err[0],\
            error_kw = dict(elinewidth=2,ecolor="black")   )

ax.bar(ind[2],renzi[0],width,color=colors[0],yerr=renzi_err[0],\
            error_kw = dict(elinewidth=2,ecolor="black")   )
ax.bar(ind[2]+width,renzi[1],width,color=colors[2],yerr=renzi_err[0],\
            error_kw = dict(elinewidth=2,ecolor="black")   )

ax.bar(ind[3],dimaio[0],width,color=colors[0],yerr=dimaio_err[0],\
            error_kw = dict(elinewidth=2,ecolor="black")   )
ax.bar(ind[3]+width,dimaio[1],width,color=colors[2],yerr=dimaio_err[0],\
            error_kw = dict(elinewidth=2,ecolor="black")   )

x = [0,1,2,3]
xlabels=["Silvio Berlusconi","Matteo Salvini","Matteo Renzi", "Luigi Di Maio"]

#plt.yticks(arange(start,end,pace))
#set the fontsize of the y-axis ticks
plt.yticks(fontsize=18)
ax.set_ylabel("Percentage %", fontsize=20)
#set 8 point for the x ticks
#plt.xticks(arange(6) + 0.12)
#tick_name = [" "," "," "," "," "," "]
#assign the ticks name
#xTickMarks=[str(x) for x in tick_name]
#set the size
#xtickNames = ax.set_xticklabels(xTickMarks)
#ax.xaxis.tick_top()
#remember to first put the labels on top of the plot and then fontsize
#otherwise it won't work- it may be a bug in matplotlib
#plt.xticks(fontsize=20)
#now set the ab,c,d,e,f,g,h on top of the plot
#ax.xaxis.set_label_position("top")
# You can specify a rotation for the tick labels in degrees or with keywords.
plt.xticks(x, xlabels, rotation=45,fontsize=18)
#grid on plot
plt.ylim(0,1)
plt.grid(True)
#legend here we need to fix the labels
ax.legend((berluP, berluN),("Positive", "Negative"),loc="upper left",fontsize=20)
#savefigure
plt.tight_layout()
plt.savefig("politics_percentage.png",dpi=300,transparent=True)
plt.savefig("politics_percentage.pdf",dpi=300)
