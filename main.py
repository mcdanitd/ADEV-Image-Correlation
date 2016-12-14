import PMDReceiver
import camFeed
import cv2
import math
import numpy
import time
#import sys, string, os

#print "opening PmdUdpDumper"
#os.system("C:/ADEV/cppToPy/src/c/build-PmdUdpDumper-Desktop_Qt_5_7_0_MinGW_32bit-Debug/debug/PmdUdpDumper.exe")


print "opening camera"
feed = camFeed.CamFeed()

print "opening PMD"
depth = PMDReceiver.PMDReceiver()

cameraMaxHorzAngle = 90
cameraMaxVertAngle = 90
depthMaxHorzAngle = 82
depthMaxVertAngle = 66
separation = 0.04269      #distance between cameras
print "Starting feed display"
depthArray = depth.getImage()
depthArray1 = numpy.zeros(depthArray.shape[:2])
depthArray2 = numpy.zeros(depthArray.shape[:2])
depthArray3 = numpy.zeros(depthArray.shape[:2])
A = numpy.zeros(depthArray.shape[:2])
#while(1):
for jrog in range(0,6):
   
        
    depthArray = depth.getImage()
    left = feed.getImage(1)
    right = feed.getImage(2)
    
    left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
    cv2.imshow('DepthImage', depthArray)
    cv2.imshow('Left', left)
    cv2.imshow('Right', right)
    
    depthArray4 = depthArray3
    depthArray3 = depthArray2
    depthArray2 = depthArray1
    depthArray1 = depthArray
    
    depthArray = (depthArray1+depthArray2+depthArray3+depthArray4)/4
    
    webcamRows, webcamColumns = left.shape[:2]    
#    leftCenterline = left[math.floor(h/2)]
    
    h, w = right.shape[:2]    
#    rightCenterline = right[math.floor(h/2)]
    
    hArray, wArray = depthArray.shape[:2]    
#    dAcenterline = depthArray[math.floor(h1/2)]
    
    
    print "sleeping"
    print jrog
    time.sleep(1)
    success = 0
    if jrog == 5:
        leftMap = numpy.zeros((hArray,wArray,2))
        rightMap = numpy.zeros((hArray,wArray,2))
    
        compArray = numpy.zeros((2,hArray,wArray))
        col=-1
        for r in range(0,hArray):         
            VertAngle = (r/hArray)*depthMaxVertAngle + (cameraMaxVertAngle-depthMaxVertAngle)/2
            lWebcamYValue = webcamRows*VertAngle/cameraMaxVertAngle
            rWebcamYValue = webcamRows*VertAngle/cameraMaxVertAngle
                    
            for c in range(0,wArray): 
                y = depthArray[r,c]   
                
                A = ((float(c)/wArray)*depthMaxHorzAngle)-(depthMaxHorzAngle/2)
               
#                x=y*math.cos(math.radians(A))
                x = y
                C = A + 90      
                wL = math.sqrt(math.pow(x,2)+math.pow(separation,2) - 2*x*separation*math.cos(math.radians(C)))
                FL = math.degrees(math.asin(separation*math.sin(math.radians(C))/wL))
                DL = 180 - FL -C
                BL = 90 - DL
                lWebcamXValue = (BL + 45)*webcamColumns/cameraMaxHorzAngle

                if (lWebcamXValue <= 640) and (lWebcamXValue>=0):
                    leftMap[r,c,0] = lWebcamYValue
                    leftMap[r,c,1] = lWebcamXValue
                    compArray[0,r,c] = left[lWebcamYValue,lWebcamXValue]
                E = 180 - C
                wR = math.sqrt(math.pow(x,2)+math.pow(separation,2) - 2*x*separation*math.cos(math.radians(E)))
                FR = math.degrees(math.asin(separation*math.sin(math.radians(E))/wR))
                DR = 180 - FL - E
                BR = DR - 90
                rWebcamXValue = (BR + 45)*webcamColumns/cameraMaxHorzAngle
                if rWebcamXValue <= 640 and rWebcamXValue>=0:
                    rightMap[r,c,0] = rWebcamYValue
                    rightMap[r,c,1] = rWebcamXValue
                    compArray[1,r,c] = right[rWebcamYValue,rWebcamXValue]
                if abs(compArray[0,r,c]-compArray[1,r,c]<50):
                    success+=1;
                    
#                    print lWebcamXValue + "," + lWebcamYValue
#                    print rWebcamXValue + "," + rWebcamYValue
               
                	#this is wrong, but close, need to throw in a factor for max vertical angle
            #    	lWebcamYValue = (yvalue/depthRows)*webcamRows
    
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
#  
#    	
#    		
#    	
#  
print float(success)/(hArray*(wArray-50))
cv2.destroyWindow("Left")
cv2.destroyWindow("Right")
cv2.destroyWindow('DepthImage')

#    for(pixel in depthArray):
#        pixel = 
#    	A = ((xvalue/depth.getCols())*depthMaxHorzAngle)-90
#    	#if distance values aren't along the hypotenuse add next line
#    	#x = pixel*cos()
#    	#otherwise
#    	x=pixel
#    
#    	# for left webcam
#    	if(A>0):
#    		C=A+90
#    	else:
#    		C = 90-A
#    	w = sqrt(x^2+separation^2 - 2*x*separation*cos(C)) # add some correction for C>90
#    	D = arcsin(x*sin(C)/w)
#    	B = 90 - D
#    	lWebcamXValue = B+90*webcamColumns/depthMaxHorzAngle
#    	#this is wrong, but close, need to throw in a factor for max vertical angle
#    	lWebcamYValue = (yvalue/depthRows)*webcamRows
    
    


