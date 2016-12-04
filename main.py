import PMDReceiver
import camFeed
import cv2
import math
import numpy

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
while(1):
    
    depthArray = depth.getImage()
    left = feed.getImage(1)
    right = feed.getImage(2)
    cv2.imshow('DepthImage', depthArray)
    cv2.imshow('Left', left)
    cv2.imshow('Right', right)
    
    
    
    h, webcamColumns = left.shape[:2]    
    leftCenterline = left[math.floor(h/2)]
    
    h, w = right.shape[:2]    
    rightCenterline = right[math.floor(h/2)]
    
    h, wArray = depthArray.shape[:2]    
    dAcenterline = depthArray[math.floor(h/2)]
    
    leftMap = numpy.zeros((1,wArray))
    for i in range(0,wArray):
    	A = ((i/depth.getCols())*depthMaxHorzAngle)-90
    	#if distance values aren't along the hypotenuse add next line
    	x = dAcenterline[i]*math.cos(math.radians(A))
    	#otherwise
#    	x=pixel
    
    	# for left webcam
    	if A > 0:
    		C=A+90
    	else:
    		C = 90-A
      
    	w = math.sqrt(x^2+separation^2 - 2*x*separation*math.cos(math.radians(C))) # add some correction for C>90
    	D = math.degrees(math.asin(x*math.sin(math.radians(C))/w))
    	B = 90 - D
    	lWebcamXValue = (B+90)*webcamColumns/cameraMaxHorzAngle
        leftMap[1,i] = lWebcamXValue
        
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
    
    


