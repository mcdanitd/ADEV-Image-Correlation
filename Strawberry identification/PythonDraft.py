# PythonDraft.py
# This script is meant to be the 

import cv2
import numpy as np
#import antigravity



#load image from file.  This will be from another class eventually
inputImage = cv2.imread('Straw 2.jpg')
image = cv2.cvtColor(inputImage, cv2.COLOR_BGR2HSV)

upperHue = 1.0*255
lowerHue = 0.7*255
lowerSat = 0.5*255
sizeThreshMin = 200    #will have to adjust as we get closer to the fruit.
sizeThreshMax = 2000   #will have to adjust as we get closer to the fruit.
# the maximum size threshold given in for this is designed to eliminate
# fruit that are bunched closely together.  We currently do not have a way
# to recognize that an image shows two overlapping strawberries.  The
# solution to this may be in using depth camera information on the objects
# that the maximum size threshold is filtering out.

dimen = np.shape(image)
#(dimen[0]).__class__.__name__
mask = np.zeros((dimen[0],dimen[1]))

if upperHue > lowerHue:	# create mask of red values
	for x in range(0, dimen[0]):
		for y in range(0, dimen[1]):
			if image[x,y,1] > lowerHue and image[x,y,1] < upperHue and image[x,y,2] > lowerSat:
				mask[x,y] = 1;
else:	#allowing for wraparound boundaries
	for x in range(0, dimen[0]):
		for y in range(0, dimen[1]):
			if image[x,y,1] > lowerHue and image[x,y,1] < upperHue and image[x,y,2] > lowerSat:
				mask[x,y] = 1;

# Morphology: erode and dilate.  Needs more work
kernel = np.ones((3,3),np.uint8)
morphed = cv2.erode(mask, kernel, iterations = 1)
morphed = cv2.dilate(morphed, kernel, iterations = 2)

# wrote a python version of MATLAB's bwlabel using pseudocode from Img. Rec. test question pseudocode
connectivity = 8
#components = cv2.connectedComponentsWithStats(morphed, connectivity, cv2.CV_32S)




while 1:
	cv2.imshow("Original Image",inputImage)
	cv2.imshow("Mask",mask)
	cv2.imshow("Morphology",morphed)
	key = cv2.waitKey(20)	#every 20 ms, checks if a key has been pressed.
	if key == 27: # exit on ESC
		break


cv2.destroyWindow("preview1")

