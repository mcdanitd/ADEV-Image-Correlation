import PMDReceiver
import camFeed
import cv2
import math
import numpy
import time

print "opening camera"
feed = camFeed.CamFeed()

print "opening PMD"
depth = PMDReceiver.PMDReceiver()

cameraMaxHorzAngle = 90
cameraMaxVertAngle = 90
depthMaxHorzAngle = 82
depthMaxVertAngle = 66
separation = .0352      #distance between cameras
print "Starting feed display"
depthArray = depth.getImage()
depthArray1 = numpy.zeros(depthArray.shape[:2])
depthArray2 = numpy.zeros(depthArray.shape[:2])
depthArray3 = numpy.zeros(depthArray.shape[:2])
#while(1):
for jrog in range(0,6):
   
        
    depthArray = depth.getImage()
    left = feed.getImage(1)
    right = feed.getImage(2)
    cv2.imshow('DepthImage', depthArray)
    cv2.imshow('Left', left)
    cv2.imshow('Right', right)
    
    depthArray4 = depthArray3
    depthArray3 = depthArray2
    depthArray2 = depthArray1
    depthArray1 = depthArray
    
    depthArray = (depthArray1+depthArray2+depthArray3+depthArray4)/4
    
    h, webcamColumns = left.shape[:2]    
#    leftCenterline = left[math.floor(h/2)]
    
    h, w = right.shape[:2]    
#    rightCenterline = right[math.floor(h/2)]
    
    h, wArray = depthArray.shape[:2]    
#    dAcenterline = depthArray[math.floor(h1/2)]
    
    
    
    print "sleeping"
    print jrog
    time.sleep(1)
    if jrog == 5:
        leftMap = numpy.zeros((1,wArray))
        rightMap = numpy.zeros((1,wArray))
    
        compArray = numpy.zeros((2,wArray,3))
        for i in range(0,wArray):
            y = depthArray[60,i]   
            if y == 0:
                pass
            else:
                A = ((i/depth.getCols())*depthMaxHorzAngle)-(depthMaxHorzAngle/2)
                
#                x=y*math.cos(math.radians(A))
                x = y
                C = A + 90                
                    
                wL = math.sqrt(math.pow(x,2)+math.pow(separation,2) - 2*x*separation*math.cos(math.radians(C)))
                DL = math.degrees(math.asin(x*math.sin(math.radians(C))/wL))
                BL = 90 - DL
                lWebcamXValue = (BL + 45)*webcamColumns/cameraMaxHorzAngle
                if (lWebcamXValue <= 640) and (lWebcamXValue>=0):
                    leftMap[0,i] = lWebcamXValue
                    compArray[0,i,:] = left[240,lWebcamXValue,:]
                E = 180 - C
                wR = math.sqrt(math.pow(x,2)+math.pow(separation,2) - 2*x*separation*math.cos(math.radians(E)))
                DR = math.degrees(math.asin(x*math.sin(math.radians(E))/wR))
                BR = 90 - DR
                rWebcamXValue = (BR + 45)*webcamColumns/cameraMaxHorzAngle
                if rWebcamXValue <= 640 and rWebcamXValue>=0:
                    rightMap[0,i] = rWebcamXValue
                    compArray[1,i,:] = right[240,rWebcamXValue,:]
                    
                print lWebcamXValue
                print rWebcamXValue
                
                
                
                
    #        	A = ((i/depth.getCols())*depthMaxHorzAngle)-90
    #        	#if distance values aren't along the hypotenuse add next line
    #        	x = y*math.cos(math.radians(A))
    #        	#otherwise
    #        #    	x=pixel
    #        
    #        	# for left webcam
    #        	if A > 0:
    #        		C=A+90
    #        	else:
    #        		C = 90-A
    #          
    #          
    #        	w = math.sqrt(math.pow(x,2)+math.pow(separation,2) - 2*x*separation*math.cos(math.radians(C))) # add some correction for C>90
    #        	D = math.degrees(math.asin(x*math.sin(math.radians(C))/w))
    #        	B = 90 - D
    #        	lWebcamXValue = (B+90)*webcamColumns/cameraMaxHorzAngle
    ##            fada = daf
    #            leftMap[0,i] = lWebcamXValue
           
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
    
    


