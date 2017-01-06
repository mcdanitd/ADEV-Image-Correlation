import PMDReceiver
import camFeed
import cv2
import math
import numpy
import time
#import sys, string, os

#print "opening PmdUdpDumper"
#os.system("C:/ADEV/cppToPy/src/c/build-PmdUdpDumper-Desktop_Qt_5_7_0_MinGW_32bit-Debug/debug/PmdUdpDumper.exe")

tolerance = 70

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
depthArray1 = depth.getImage()
depthArray2 = depth.getImage()
depthArray3 = depth.getImage()
A = numpy.zeros(depthArray.shape[:2])
loops = 0
successHistory = 0
mid50SuccessHistory = 0
mid25SuccessHistory = 0

#depthimagefile = 0;

while(1):
    
    loops+=1
        
    depthArray = depth.getImage()
    left = feed.getImage(1)
    right = feed.getImage(2)
    
    left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
    
    depthArray4 = depthArray3
    depthArray3 = depthArray2
    depthArray2 = depthArray1
    depthArray1 = depthArray
    
    depthArray = (depthArray1*4+depthArray2*3+depthArray3*2+depthArray4)/10
    
#    depthArray = cv2.fromarray(depthArray)
#    depthArray = cv2.medianBlur(depthArray,3)
    
    cv2.imshow('DepthImage', depthArray)
    cv2.imshow('Left', left)
    cv2.imshow('Right', right)
    
    
    webcamRows, webcamColumns = left.shape[:2]    
#    leftCenterline = left[math.floor(h/2)]
    
    h, w = right.shape[:2]
#    rightCenterline = right[math.floor(h/2)]
    
    hArray, wArray = depthArray.shape[:2]    
#    dAcenterline = depthArray[math.floor(h1/2)]
    
#    
#    print "sleeping"
#    print jrog
#    time.sleep(1)
    success = 0
    middle50Success = 0
    middle25Success = 0
#    if jrog == 5:
    leftMap = numpy.zeros((hArray,wArray,2))
    rightMap = numpy.zeros((hArray,wArray,2))
    leftInverseMap = numpy.zeros((webcamRows,webcamColumns,1))
    rightInverseMap = numpy.zeros((webcamRows,webcamColumns,1))

    errors = numpy.zeros((hArray,wArray),dtype=int)
    
    compArray = numpy.zeros((2,hArray,wArray), dtype=numpy.uint8)
    midCompArray = numpy.zeros((2,hArray/2,wArray/2))
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

            if (lWebcamXValue < w) and (lWebcamXValue>=0):
                leftMap[r,c,0] = lWebcamYValue
                leftMap[r,c,1] = lWebcamXValue
                compArray[0,r,c] = int(left[lWebcamYValue,lWebcamXValue])
                leftInverseMap[lWebcamYValue,lWebcamXValue] = x
#                
#                    midCompArray[0,r-hArray/4,c-wArray/4] = left[lWebcamYValue,lWebcamXValue]
                    
            E = 180 - C
            wR = math.sqrt(math.pow(x,2)+math.pow(separation,2) - 2*x*separation*math.cos(math.radians(E)))
            FR = math.degrees(math.asin(separation*math.sin(math.radians(E))/wR))
            DR = 180 - FL - E
            BR = DR - 90
            rWebcamXValue = (BR + 45)*webcamColumns/cameraMaxHorzAngle
            if rWebcamXValue < w and rWebcamXValue>=0:
                rightMap[r,c,0] = rWebcamYValue
                rightMap[r,c,1] = rWebcamXValue
                compArray[1,r,c] = int(right[rWebcamYValue,rWebcamXValue])
                rightInverseMap[rWebcamYValue,rWebcamXValue] = x
                
            if abs(compArray[0,r,c]-compArray[1,r,c]<tolerance):
                success+=1
                if (r>hArray/4)and(r<hArray*3/4)and(c>wArray/4)and(c<wArray*3/4):
                    middle50Success+=1
                if (r>3*hArray/8)and(r<hArray*5/8)and(c>wArray*3/8)and(c<wArray*5/8):
                    middle25Success+=1
            else:
                errors[r,c]=255;
                    
    print loops
    successRate = float(success)/(hArray*wArray)
    print successRate
    mid50SuccessRate = float(middle50Success)/((hArray*wArray)/4)
    print mid50SuccessRate
    mid25SuccessRate = float(middle25Success)/((hArray*wArray)/16)
    print mid25SuccessRate
    successHistory = float(successRate+(successHistory*(loops-1)))/loops
    print successHistory
    mid50SuccessHistory = float(mid50SuccessRate+(mid50SuccessHistory*(loops-1)))/loops
    print mid50SuccessHistory
    mid25SuccessHistory = float(mid25SuccessRate+(mid25SuccessHistory*(loops-1)))/loops
    print mid25SuccessHistory
    
    dualMap = ((compArray[1,:,:])+(compArray[0,:,:]))/2
    dualMap = cv2.cvtColor(dualMap,cv2.COLOR_GRAY2BGR)
    errLoc = numpy.where(errors==255)
#    for r in range(0,hArray):
#        for c in range(0,wArray): 
#            if errors[r,c]==255:
#                dualMap[r,c,:]=[0,0,255];    
#    
    cv2.imshow('Compare', dualMap)    
    
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
#        depthimagefile+=1;
#        scaler = 255
#        depthArray = depthArray*scaler
#        filename = 'C:/ADEV/WinPython-64bit-2.7.10.3/python-2.7.10.amd64/Scripts/ADEV/depthImages/' + str(depthimagefile) + '.tiff'
#        cv2.imwrite(filename, depthArray)
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
    
    


