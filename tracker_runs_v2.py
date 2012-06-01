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
    fig3 = plt.figure(3)
    ax3 = fig3.add_subplot(111,projection='3d')



    def fittedline(xo,yo,zo,xn,yn,zn):
    	x = np.linspace(xo,xn,100) 
    	y = np.linspace(yo,yn,100) 
    	z = np.linspace(zo,zn,100)
	ax2.plot(x, y, z, c='b', linewidth = 2)
	ax3.plot(x, y, z, c='b', linewidth = 2)    





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
        if len(event_lists[i]) > 4:
            (A,B) = fl.bestline(event_lists[i],acc=0.01,partition=4,recurse='half')   
            points_fitted_start.append(A)
            points_fitted_end.append(B)


    ii=0
    while ii < len(points_fitted_start):
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
        for i in range(len(event_lists[q])):
            xs.append(event_lists[q][i].x)
            ys.append(event_lists[q][i].y)
            zs.append(event_lists[q][i].z)
# plotting these new scatter points
    ax2.scatter(xs,ys,zs,c='k',marker='o')
    ax3.scatter(xs,ys,zs,c='k',marker='o')
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
    print len(xm), len(xs)
    print "x range =",min(xm),",", max(xm) 
    print "y range =",min(ym),",", max(ym) 
    print "z range =",min(zm),",", max(zm) 
    print '==================================\n'
    print "Data is given as 2 points on the fit line"
    print "Format (x, y, z, 0.00)"
    iii=0
    while iii < len(points_fitted_start):
        print "Fit #",iii, points_fitted_start[iii],points_fitted_end[iii]
        iii += 1
    pfs = points_fitted_start
    pfe = points_fitted_end
    filenme = 'output' + str(event) + '.txt'
    FILE = open(filenme,'w')
    ev = '##### Event ' + str(event) +'\n'
    FILE.write(ev)
    sp = ' '
    nl = '\n'
    index = 0
    for i in range(len(event_lists)):
        if len(event_lists[i]) > 4:
            tempstr = '####Fit list #' + str(index + 1) + '\n'
            FILE.write(tempstr)
            tempstr = '####Fit points: \n'
            FILE.write(tempstr)
            tempstr = '###(' + str(pfs[index].x) + ',' + str(pfs[index].y) + ',' + str(pfs[index].z) + ')\n' 
            FILE.write(tempstr)
            tempstr = '###(' + str(pfe[index].x) + ',' + str(pfe[index].y) + ',' + str(pfe[index].z) + ')\n'
            FILE.write(tempstr)
            tempstr = '#Data!\n'
            FILE.write(tempstr)
            for j in range(len(event_lists[i])):
                dg = str(event_lists[i][j].x) + sp + str(event_lists[i][j].y) + sp + str(event_lists[i][j].z) + sp + str(event_lists[i][j].adc) + nl
                FILE.write(dg)
            index += 1
    f = FILE.close()
    
    plt.show()


