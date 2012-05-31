import dataPackage as dPg
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import math

def separateData(event, pkg, fileNme):
	###Pre-conditions to be set.
	n = event #event number
	#fileNme = 'alphas.dat'
	maxDistFromLine = 0.7 #When looking for points  how far away from the
							#hypothetical line should we still consider
							#them to be on the same line.
							
	###########################################################

	#Opens Package
	#pkg = dPg.package(fileNme)

	#Put raw data from file into 2D array to make it easier to index.
	f = open(fileNme)
	dataArr = []
	L = -1
	point = 0
	initDir = -1
	for line in f:
		if line[0] == '#':
			L += 1
		elif L == n:
			x = line
			x = x[:len(x)-1]
			x = x.split(' ')
			i = 0
			for num in x:
				x[i] = int(x[i])
				if i == 0:
					volume = x[i]
				elif i == 1:
					row = x[i]
				elif i == 2:
					column = x[i]
				elif i == 3:
					bucket = x[i]
				elif i == 4:
					adc = x[i]
				i += 1
			dataArr.append(np.array([volume, row, column, bucket, adc, initDir, 0]))
			point += 1

	print 'Number of points in list:', len(dataArr)
	#Go through all the points in the event list and find the extreme points
	minXElement = 0
	for i in range(len(pkg[n])):
		if pkg[n][i].x < pkg[n][minXElement].x:
			minXElement = i

	maxXElement = 0
	for i in range(len(pkg[n])):
		if (pkg[n][i].x > pkg[n][maxXElement].x):
			maxXElement = i

	minYElement = 0
	for i in range(len(pkg[n])):
		if pkg[n][i].y < pkg[n][minYElement].y:
			minYElement = i
			
	maxYElement = 0
	for i in range(len(pkg[n])):
		if pkg[n][i].y > pkg[n][maxYElement].y:
			maxYElement = i

	minZElement = 0
	for i in range(len(pkg[n])):
		if pkg[n][i].z < pkg[n][minZElement].z:
			minZElement = i
			
	maxZElement = 0
	for i in range(len(pkg[n])):
		if pkg[n][i].z > pkg[n][maxZElement].z:
			maxZElement = i

	#Print out all of the extreme points
	print 'min X point',minXElement,': (', pkg[n][minXElement].x, ',',
	print pkg[n][minXElement].y, ',', pkg[n][minXElement].z, ')',
	print ' with an ADC of: ', pkg[n][minXElement].adc

	print 'max X point',maxXElement,': (', pkg[n][maxXElement].x, ',',
	print pkg[n][maxXElement].y, ',', pkg[n][maxXElement].z, ')',
	print ' with an ADC of: ', pkg[n][maxXElement].adc

	print 'min Y point',minYElement,': (', pkg[n][minYElement].x, ',',
	print pkg[n][minYElement].y, ',', pkg[n][minYElement].z, ')',
	print ' with an ADC of: ', pkg[n][minYElement].adc

	print 'max Y point',maxYElement,': (', pkg[n][maxYElement].x, ',',
	print pkg[n][maxYElement].y, ',', pkg[n][maxYElement].z, ')',
	print ' with an ADC of: ', pkg[n][maxYElement].adc

	print 'min Z point',minZElement,': (', pkg[n][minZElement].x, ',',
	print pkg[n][minZElement].y, ',', pkg[n][minZElement].z, ')',
	print ' with an ADC of: ', pkg[n][minZElement].adc

	print 'max Z point',maxZElement,': (', pkg[n][maxZElement].x, ',',
	print pkg[n][maxZElement].y, ',', pkg[n][maxZElement].z, ')',
	print ' with an ADC of: ', pkg[n][maxZElement].adc

	#Now lets think about constructing the gradient...
	#know that the points are sorted in the list by x, y, then z.
	#For the gradient the following are the definitions for traversing:
	# -1 : Initialized but no value
	#  0 : This point is max (at top of gradient)
	#  1 : max in +x direction
	#  2 : max in -x direction 
	#  3 : max in +y direction
	#  4 : max in -y direction 
	#  5 : max in +z direction
	#  6 : max in -z direction 

	for i in range(len(dataArr)):
	#	print dataArr[i]
		plusx = 0
		minusx = 0
		plusy = 0
		minusy = 0
		plusz = 0
		minusz = 0
		index = i - 1
		if index >= 0 and dataArr[index][1] == dataArr[i][1] and dataArr[index][2] == dataArr[i][2] and dataArr[index][3] == (dataArr[i][3] - 1):
			minusz = dataArr[index][4]
			index -= index
		while index >= 0:
			if dataArr[index][1] == dataArr[i][1] and dataArr[index][2] == (dataArr[i][2] - 1) and dataArr[index][3] == dataArr[i][3]:
				minusy = dataArr[index][4]
			if dataArr[index][1] == (dataArr[i][1] - 1) and dataArr[index][2] == dataArr[i][2] and dataArr[index][3] == dataArr[i][3]:
				minusx = dataArr[index][4]
			index-=1
		index = i + 1
		if index < len(dataArr) and dataArr[index][1] == dataArr[i][1] and dataArr[index][2] == dataArr[i][2] and dataArr[index][3] == (dataArr[i][3] + 1):
			plusz = dataArr[index][4]
			index += index
		while index < len(dataArr):
			if dataArr[index][1] == dataArr[i][1] and dataArr[index][2] == (dataArr[i][2] + 1) and dataArr[index][3] == dataArr[i][3]:
				plusy = dataArr[index][4]
			if dataArr[index][1] == (dataArr[i][1] + 1) and dataArr[index][2] == dataArr[i][2] and dataArr[index][3] == dataArr[i][3]:
				plusx = dataArr[index][4]
			index+=1
		maxDir = 0
		maxVal = dataArr[i][4]
		if plusx > maxVal:
			maxVal = plusx
			maxDir = 1
		if minusx > maxVal:
			maxVal = minusx
			maxDir = 2
		if plusy > maxVal:
			maxVal = plusy
			maxDir = 3
		if minusy > maxVal:
			maxVal = minusy
			maxDir = 4
		if plusz > maxVal:
			maxVal = plusz
			maxDir = 5
		if minusz > maxVal:
			maxVal = minusz
			maxDir = 6
		
		dataArr[i][5] = maxDir
		
	output = []
	outputArr = []
	for i in range(len(dataArr)):
		if dataArr[i][5] == 0:
			output.append(pkg[n][i])
			outputArr.append(dataArr[i])
			
	#below graphs the two different data sets.
	
	#fig = plt.figure()
	#ax = fig.add_subplot(111, projection='3d')

	# Variables==============================

	hp_filter=0 # this will filter points with adc< value (high pass)
	#high pass means that values higher pass the check and lower are filtered
	#this is counter intutive for the phrase "filter"



	#==========================================

	xi=[]
	zi=[]
	yi=[]
	ii=0
	while ii < len(output):
		if hp_filter <= output[ii].adc:
			xi.append(output[ii].x)
			yi.append(output[ii].y)
			zi.append(output[ii].z)
			ii=ii+1
		else:
			ii=ii+1



	#c='g'
	#m='o'
	#ax.scatter(xi, yi, zi, c=c, marker=m)

	#ax.set_xlabel('X = Row')
	#ax.set_ylabel('Y = column')
	#ax.set_zlabel('Z = Bucket')
	#plt.show()



	#fig1 = plt.figure()
	#ax1 = fig1.add_subplot(111, projection='3d')

	xs=[]
	zs=[]
	ys=[]
	i=0
	while i < len(pkg[n]):
		if hp_filter <= pkg[n][i].adc:
			xs.append(pkg[n][i].x)
			ys.append(pkg[n][i].y)
			zs.append(pkg[n][i].z)
			
		i += 1


	#c='g'
	#m='o'
	#ax1.scatter(xs, ys, zs, c=c, marker=m)

	#ax1.set_xlabel('X = Row')
	#ax1.set_ylabel('Y = column')
	#ax1.set_zlabel('Z = Bucket')

	print
	print 'Less data due to filtering using gradient...'
	print 'Number of points in list:', len(outputArr)
	#Go through all the points in the event list and find the extreme points
	minXElement = 0
	for i in range(len(outputArr)):
		if output[i].x < output[minXElement].x:
			minXElement = i

	maxXElement = 0
	for i in range(len(outputArr)):
		if (output[i].x > output[maxXElement].x):
			maxXElement = i

	minYElement = 0
	for i in range(len(outputArr)):
		if output[i].y < output[minYElement].y:
			minYElement = i
			
	maxYElement = 0
	for i in range(len(outputArr)):
		if output[i].y > output[maxYElement].y:
			maxYElement = i

	minZElement = 0
	for i in range(len(outputArr)):
		if output[i].z < output[minZElement].z:
			minZElement = i
			
	maxZElement = 0
	for i in range(len(outputArr)):
		if output[i].z > output[maxZElement].z:
			maxZElement = i

	#Print out all of the extreme points
	print 'min X point',minXElement,': (', output[minXElement].x, ',',
	print output[minXElement].y, ',', output[minXElement].z, ')',
	print ' with an ADC of: ', output[minXElement].adc

	print 'max X point',maxXElement,': (', output[maxXElement].x, ',',
	print output[maxXElement].y, ',', output[maxXElement].z, ')',
	print ' with an ADC of: ', output[maxXElement].adc

	print 'min Y point',minYElement,': (', output[minYElement].x, ',',
	print output[minYElement].y, ',', output[minYElement].z, ')',
	print ' with an ADC of: ', output[minYElement].adc

	print 'max Y point',maxYElement,': (', output[maxYElement].x, ',',
	print output[maxYElement].y, ',', output[maxYElement].z, ')',
	print ' with an ADC of: ', output[maxYElement].adc

	print 'min Z point',minZElement,': (', output[minZElement].x, ',',
	print output[minZElement].y, ',', output[minZElement].z, ')',
	print ' with an ADC of: ', output[minZElement].adc
	
	print 'max Z point',maxZElement,': (', output[maxZElement].x, ',',
	print output[maxZElement].y, ',', output[maxZElement].z, ')',
	print ' with an ADC of: ', output[maxZElement].adc
	print
	
	lists = []
	index = 0
	usedPnts = 0
	while usedPnts < len(output) - 5:
		print 'Finding line number', (index + 1), 'in event', n, '... using minx'
		lists.append([])
		minXElement = -1
		for i in range(len(outputArr)):
			if outputArr[i][6] == 0:
				if minXElement == -1:
					minXElement = i
				if output[i].x < output[minXElement].x:
					minXElement = i
		
		stPnt = minXElement
		outputArr[stPnt][6] = 1
		lists[index].append(output[stPnt])
		
		minDist = 1000.0
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if  tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point1 = minIndex
		outputArr[point1][6] = 1
		lists[index].append(output[point1])
        
		minDist = 1000
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point2 = minIndex
		outputArr[point2][6] = 1
		lists[index].append(output[point2])
        
		minDist = 1000
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point3 = minIndex
		outputArr[point3][6] = 1
		lists[index].append(output[point3])
		
		lastPnt = point3
        
		print 'Index of four closest points:', point1, point2, point3
		vector = np.array([0.0,0.0,0.0])
		x0 = output[stPnt].x
		y0 = output[stPnt].y
		z0 = output[stPnt].z
		
		x = output[point1].x
		y = output[point1].y
		z = output[point1].z
		vector[0] = (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] = (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] = (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		x = output[point2].x
		y = output[point2].y
		z = output[point2].z
		vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		x = output[point3].x
		y = output[point3].y
		z = output[point3].z
		vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		usedPnts += 4
		pntsInLst = 4
		
		mveVtr = []
		mveVtr.append(vector[0]/(pntsInLst - 1))
		mveVtr.append(vector[1]/(pntsInLst - 1))
		mveVtr.append(vector[2]/(pntsInLst - 1))
        
		pnt = []
		pnt.append(x0)
		pnt.append(y0)
		pnt.append(z0)
		
		while pnt[0] < 6:
			for i in range(len(output)):
				if outputArr[i][6] == 0:
					x = output[i].x
					y = output[i].y
					z = output[i].z
					
					if ((x - pnt[0])**2 + (y - pnt[1])**2 + (z - pnt[2])**2)**(0.5) < maxDistFromLine:
						outputArr[i][6] = 1
						vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						mveVtr[0] = vector[0]/(pntsInLst - 1)
						mveVtr[1] = vector[1]/(pntsInLst - 1)
						mveVtr[2] = vector[2]/(pntsInLst - 1)
						lists[index].append(output[i])
						usedPnts += 1
						pntsInLst += 1
			pnt[0] += mveVtr[0]
			pnt[1] += mveVtr[1]
			pnt[2] += mveVtr[2]
		index += 1
		
	for i in range(len(lists)):
		print 'List', (i+1)
		for j in range(len(lists[i])):
		    print '(',lists[i][j].x,',',lists[i][j].y,',',lists[i][j].z,')'
	
	for i in range(len(outputArr)):
		outputArr[i][6] = 0
		
	listsy = []
	index = 0
	usedPnts = 0
	while usedPnts < len(output) - 5:
		print 'Finding line number', (index + 1), 'in event', n, '...(using miny)'
		listsy.append([])
		minXElement = -1
		for i in range(len(outputArr)):
			if outputArr[i][6] == 0:
				if minXElement == -1:
					minXElement = i
				if output[i].y < output[minXElement].y:
					minXElement = i
		
		stPnt = minXElement
		outputArr[stPnt][6] = 1
		listsy[index].append(output[stPnt])
		
		minDist = 1000.0
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if  tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point1 = minIndex
		outputArr[point1][6] = 1
		listsy[index].append(output[point1])
        
		minDist = 1000
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point2 = minIndex
		outputArr[point2][6] = 1
		listsy[index].append(output[point2])
        
		minDist = 1000
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point3 = minIndex
		outputArr[point3][6] = 1
		listsy[index].append(output[point3])
		
		lastPnt = point3
        
		print 'Index of four closest points:', point1, point2, point3
		vector = np.array([0.0,0.0,0.0])
		x0 = output[stPnt].x
		y0 = output[stPnt].y
		z0 = output[stPnt].z
		
		x = output[point1].x
		y = output[point1].y
		z = output[point1].z
		vector[0] = (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] = (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] = (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		x = output[point2].x
		y = output[point2].y
		z = output[point2].z
		vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		x = output[point3].x
		y = output[point3].y
		z = output[point3].z
		vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		usedPnts += 4
		pntsInLst = 4
		
		mveVtr = []
		mveVtr.append(vector[0]/(pntsInLst - 1))
		mveVtr.append(vector[1]/(pntsInLst - 1))
		mveVtr.append(vector[2]/(pntsInLst - 1))
        
		pnt = []
		pnt.append(x0)
		pnt.append(y0)
		pnt.append(z0)
		
		while pnt[1] < 6:
			for i in range(len(output)):
				if outputArr[i][6] == 0:
					x = output[i].x
					y = output[i].y
					z = output[i].z
					
					if ((x - pnt[0])**2 + (y - pnt[1])**2 + (z - pnt[2])**2)**(0.5) < maxDistFromLine:
						outputArr[i][6] = 1
						vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						mveVtr[0] = vector[0]/(pntsInLst - 1)
						mveVtr[1] = vector[1]/(pntsInLst - 1)
						mveVtr[2] = vector[2]/(pntsInLst - 1)
						listsy[index].append(output[i])
						usedPnts += 1
						pntsInLst += 1
			pnt[0] += mveVtr[0]
			pnt[1] += mveVtr[1]
			pnt[2] += mveVtr[2]
		index += 1
	
	for i in range(len(listsy)):
		print 'yList', (i+1)
		for j in range(len(listsy[i])):
			print '(',listsy[i][j].x,',',listsy[i][j].y,',',listsy[i][j].z,')'
	
	for i in range(len(outputArr)):
		outputArr[i][6] = 0
		
	listsz = []
	index = 0
	usedPnts = 0
	while usedPnts < len(output) - 5:
		print 'Finding line number', (index + 1), 'in event', n, '... using minz'
		listsz.append([])
		minXElement = -1
		for i in range(len(outputArr)):
			if outputArr[i][6] == 0:
				if minXElement == -1:
					minXElement = i
				if output[i].z < output[minXElement].z:
					minXElement = i
		
		stPnt = minXElement
		outputArr[stPnt][6] = 1
		listsz[index].append(output[stPnt])
		
		minDist = 1000.0
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if  tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point1 = minIndex
		outputArr[point1][6] = 1
		listsz[index].append(output[point1])
        
		minDist = 1000
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point2 = minIndex
		outputArr[point2][6] = 1
		listsz[index].append(output[point2])
        
		minDist = 1000
		minIndex = -1
		for j in range(len(outputArr)):
			tempDist = ((output[j].x - output[stPnt].x)**2 + (output[j].y - output[stPnt].y)**2 + (output[j].z - output[stPnt].z)**2)**(0.5)
			if tempDist < minDist and outputArr[j][6] == 0:
				minDist = tempDist
				minIndex = j
		point3 = minIndex
		outputArr[point3][6] = 1
		listsz[index].append(output[point3])
		
		lastPnt = point3
        
		print 'Index of four closest points:', point1, point2, point3
		vector = np.array([0.0,0.0,0.0])
		x0 = output[stPnt].x
		y0 = output[stPnt].y
		z0 = output[stPnt].z
		
		x = output[point1].x
		y = output[point1].y
		z = output[point1].z
		vector[0] = (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] = (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] = (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		x = output[point2].x
		y = output[point2].y
		z = output[point2].z
		vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		x = output[point3].x
		y = output[point3].y
		z = output[point3].z
		vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
		
		usedPnts += 4
		pntsInLst = 4
		
		mveVtr = []
		mveVtr.append(vector[0]/(pntsInLst - 1))
		mveVtr.append(vector[1]/(pntsInLst - 1))
		mveVtr.append(vector[2]/(pntsInLst - 1))
        
		pnt = []
		pnt.append(x0)
		pnt.append(y0)
		pnt.append(z0)
		
		while pnt[2] < 6:
			for i in range(len(output)):
				if outputArr[i][6] == 0:
					x = output[i].x
					y = output[i].y
					z = output[i].z
					
					if ((x - pnt[0])**2 + (y - pnt[1])**2 + (z - pnt[2])**2)**(0.5) < maxDistFromLine:
						outputArr[i][6] = 1
						vector[0] += (x-x0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						vector[1] += (y-y0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						vector[2] += (z-z0)/(((x0-x)**2+(y0-y)**2+(z0-z)**2)**(0.5))
						mveVtr[0] = vector[0]/(pntsInLst - 1)
						mveVtr[1] = vector[1]/(pntsInLst - 1)
						mveVtr[2] = vector[2]/(pntsInLst - 1)
						listsz[index].append(output[i])
						usedPnts += 1
						pntsInLst += 1
			pnt[0] += mveVtr[0]
			pnt[1] += mveVtr[1]
			pnt[2] += mveVtr[2]
		index += 1
	
	for i in range(len(listsz)):
		print 'zList', (i+1)
		for j in range(len(listsz[i])):
		    print '(',listsz[i][j].x,',',listsz[i][j].y,',',listsz[i][j].z,')'
	
	if len(listsy) < len(lists):
		lists = listsy
	if len(listsz) < len(lists):
		lists = listsz
		
	#plt.show()
	return lists
