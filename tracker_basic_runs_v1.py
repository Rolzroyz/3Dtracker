# 3D tracker with visualization
from dataPackage import *
pkg = package('NIFFTE-alphas.dat')

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

import fitLine as fl
import edgefnd_v1 as ef



def run():
# import data and plotting packages




    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(111,projection='3d')
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111,projection='3d')



    def fittedline(xo,yo,zo,xn,yn,zn):
    	x = np.linspace(xo,xn,100) 
    	y = np.linspace(yo,yn,100) 
    	z = np.linspace(zo,zn,100)
	ax2.plot(x, y, z, c='b')  





# ========================================

#hp_filter=2  # high pass filter takes out points with adc< value

# user input: event 
    prompt1 = 'Hi!\nEnter number of event (from 0 to 99) you would like to see:\n >'
    event = int(raw_input(prompt1))

#event=4

# ========================================



    event_lists = ef.separateData(event, pkg, 'NIFFTE-alphas.dat')



    xi,yi,zi =[],[],[]

    xs,ys,zs=[],[],[]

    i = 0
    points_fitted_start=[]
    points_fitted_end=[]
    for i in range(0,len(event_lists)):			# for each point in event
        (A,B) = fl.bestline(event_lists[i],acc=0.01,partition=4,recurse='half')   
        points_fitted_start.append(A)
        points_fitted_end.append(B)



    ii=0
    while ii < len(event_lists):
        fittedline(points_fitted_start[ii].x,points_fitted_start[ii].y,points_fitted_start[ii].z,points_fitted_end[ii].x,points_fitted_end[ii].y,points_fitted_end[ii].z)
        ii += 1

    xm,ym,zm=[],[],[]
    for q in range(len(pkg[event])):
       	xm.append(pkg[event][q].x)
	ym.append(pkg[event][q].y)
	zm.append(pkg[event][q].z)
# plotting these new scatter points

    ax1.scatter(xm,ym,zm,c='g',marker='^')
    ax1.set_xlim(-6, 6)
    ax1.set_ylim(-6, 6)
    ax1.set_zlim(-6, 6)
    ax1.set_xlabel('X (cm)')
    ax1.set_ylabel('Y (cm)')
    ax1.set_zlabel('Z (cm)')
    ax1.set_title('Event '+str(event))

    for q in range(len(event_lists)):
    	xs.append(event_lists[0][q].x)
    	ys.append(event_lists[0][q].y)
    	zs.append(event_lists[0][q].z)
# plotting these new scatter points
    ax2.scatter(xm,ym,zm,c='r',marker='o')
#ax2.set_xlim(-.01, .01)
#ax2.set_ylim(-.01, .01)
#ax2.set_zlim(-.01, .01)
    ax2.set_xlim(-6, 6)
    ax2.set_ylim(-6, 6)
    ax2.set_zlim(-6, 6)
    ax2.set_xlabel('X (cm)')
    ax2.set_ylabel('Y (cm)')
    ax2.set_zlabel('Z (cm)')
    ax2.set_title('Event '+str(event))

    print 'Event',event,'\n'
    print "x range =",min(xm),",", max(xm) 
    print "y range =",min(ym),",", max(ym) 
    print "z range =",min(zm),",", max(zm) 

    plt.show()


