
import cv2
import numpy as np
#import antigravity
import time
import datetime

fileName1 = "image1"



#sizeThreshMin = 200    #will have to adjust as we get closer to the fruit.
#sizeThreshMax = 2000   #will have to adjust as we get closer to the fruit.


cv2.namedWindow("preview")
vc1 = cv2.VideoCapture(0)

if vc1.isOpened(): # try to get the first frame
    rval1, frame1 = vc1.read()
    pixels1 = frame1.data
else:
    rval1 = False


while rval1:
	#code to store frame as an unique image here
	newImage1 = np.copy(frame1);
	dimen = np.shape(newImage1)
	now = datetime.datetime.now()
	tempfileName1 = str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + ".png"
	cv2.imwrite(tempfileName1, newImage1)
    
    #code to store information in a .txt file
	f= open(str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + ".txt","w+")
	f.write(str(now))
	f.write("\n")
    
    #identify strawberries
    
	imageHSV = cv2.cvtColor(newImage1, cv2.COLOR_BGR2HSV)
	
	#create a binary mask of potential strawberry pixels
	
	#blue = newImage1[:,:,0]
	#green = newImage1[:,:,1]
	#red = newImage1[:,:,2]
	#upperBound = 255
	#lowerBound = 100
	#retHue, threshRed = cv2.threshold(red,lowerBound,upperBound,cv2.THRESH_BINARY)
	#retHue, threshBlue = cv2.threshold(blue,lowerBound,upperBound,cv2.THRESH_BINARY)
	#retHue, threshGreen = cv2.threshold(green,lowerBound,upperBound,cv2.THRESH_BINARY)
    
	#hue = imageHSV[:,:,0]
	#sat = imageHSV[:,:,1]
	#value = imageHSV[:,:,2]
	
	redMin1 = np.array([0, 100, 0],np.uint8)	#Hue ranges 0-180, Saturation ranges 0-255, Value ranges 0-255
	redMax1 = np.array([5, 255, 225],np.uint8)

	redMin2 = np.array([160, 50, 0],np.uint8)
	redMax2 = np.array([179, 255, 225],np.uint8)

	red1 = cv2.inRange(imageHSV, redMin1, redMax1)
	red2 = cv2.inRange(imageHSV, redMin2, redMax2)
	
	threshRed = np.zeros_like(red1)
	cv2.bitwise_or(red1, red2, threshRed, mask=None)
	
	#retHue, threshHue = cv2.threshold(hue,lowerHue,upperHue,cv2.THRESH_BINARY)
	#retSat, threshSat = cv2.threshold(sat,lowerSat,255,cv2.THRESH_BINARY)
    
    #combine hue and saturation thresholding
	#red = np.zeros((dimen[0], dimen[1]))
	#for x in range(0,dimen[0]-1):
	#	for y in range(0,dimen[1]-1):
	#		red[x,y] = int(hue[x,y]*sat[x,y])
	#red = threshHue
	
	#Morphological open, kernel will likely need to be tweaked.  It might be worth it for ADEV to look into using a custom kernel
	kernel = np.ones((3,3),np.uint8)
	morphed = cv2.erode(threshRed, kernel, iterations = 2)
	morphed = cv2.dilate(morphed, kernel, iterations = 3)
	
	#Connected components count.  How many strawberries are there, find centroids
	connectivity = 8
	components = cv2.connectedComponentsWithStats(morphed, connectivity, cv2.CV_32S)
	centroids = components[3]	#centroids of x and y values.  each row is a new "strawberry"'s cemtroid
	count = np.shape(centroids)
    
	#run a loop to write a line for each distinct strawberry
	if(count[0] == 0):
		f.write("No Strawberries Found")

	for x in range(0,count[0]):
		strawberryString = "Strawberry at coordinates " + str(centroids[x,0]) + " , " + str(centroids[x,1])
		f.write(strawberryString)
		f.write("\n")
	
	#REMOVE WHEN DONE
	tempfileName2 = str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + "Morphed.png"
	cv2.imwrite(tempfileName2, morphed)
	tempfileName3 = str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + "Reds.png"
	cv2.imwrite(tempfileName3, threshRed)

	img = cv2.imread(fileName1+".jpg")
    # read new image

	cv2.imshow("preview",img)
	rval, frame = vc1.read()
	key = cv2.waitKey(20)	#every 20 ms, checks if a key has been pressed.
	if key == 27: # exit on ESC
		break
		
	
    
cv2.destroyWindow("preview")
