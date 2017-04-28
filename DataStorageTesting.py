
import cv2
import numpy as np
#import antigravity
import time
import datetime

fileName1 = "image1"


#upperHue = 1.0*255
#lowerHue = 0.7*255
#lowerSat = 0.5*255
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
    now = datetime.datetime.now()
    tempfileName1 = str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + ".png"
    cv2.imwrite(tempfileName1, newImage1)
    
    #code to store information in a .txt file
    f= open(str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + ".txt","w+")
    f.write(str(now))
    f.write("\n")
    
    #TODO: identify strawberries
    #imageHSV = cv2.cvtColor(newImage1, cv2.COLOR_BGR2HSV)
    #dimen = np.shape(imageHSV)
    #mask = np.zeros((dimen[0],dimen[1]))
    
    #if upperHue > lowerHue:	# create mask of red values
    #    for x in range(0, dimen[0]):
    #        for y in range(0, dimen[1]):
    #            if imageHSV[x,y,1] > lowerHue and imageHSV[x,y,1] < upperHue and imageHSV[x,y,2] > lowerSat:
    #                mask[x,y] = 1
	#else:#allowing for wraparound boundaries
	#	for x in range(0, dimen[0]):
	#		for y in range(0, dimen[1]):
	#			if imageHSV[x,y,1] > lowerHue and imageHSV[x,y,1] < upperHue and imageHSV[x,y,2] > lowerSat:
	#				mask[x,y] = 1;
	
	#create a binary mask of potential strawberry pixels
    reds = newImage1[:,:,2]
    ret, thresh = cv2.threshold(reds,100,200,cv2.THRESH_BINARY)	#maybe add a a green and a blue one and do logic to find pixels that are red but not blue or green
	
	#Morphological open, will likely need to be tweaked
    kernel = np.ones((3,3),np.uint8)
    morphed = cv2.erode(thresh, kernel, iterations = 1)
    morphed = cv2.dilate(morphed, kernel, iterations = 1)
	
	#Connected components count.  How many strawberries are there, find centroids
    connectivity = 8
    components = cv2.connectedComponentsWithStats(thresh, connectivity, cv2.CV_32S)
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
    tempfileName2 = str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + "Mask.png"
    cv2.imwrite(tempfileName2, morphed)
    tempfileName3 = str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + "Reds.png"
    cv2.imwrite(tempfileName3, reds)
    tempfileName3 = str(now.year)+"_"+str(now.month)+"_"+str(now.day)+"_"+str(now.hour)+"_"+str(now.minute)+"_"+str(now.second) + "Thresh.png"
    cv2.imwrite(tempfileName3, thresh)

    img = cv2.imread(fileName1+".jpg")  
    # read new image

    cv2.imshow("preview",img)
    rval, frame = vc1.read()
    key = cv2.waitKey(20)	#every 20 ms, checks if a key has been pressed.
    if key == 27: # exit on ESC
        break
		
	
    
cv2.destroyWindow("preview")
