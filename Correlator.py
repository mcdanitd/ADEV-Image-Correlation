import PMDReceiver
import camFeed
import cv2
import math
import numpy
import time
import numpy as np
#import sys, string, os

#print "opening PmdUdpDumper"
#os.system("C:/ADEV/cppToPy/src/c/build-PmdUdpDumper-Desktop_Qt_5_7_0_MinGW_32bit-Debug/debug/PmdUdpDumper.exe")

class Correlator:
    
    def __init__(self):
        
        self.tolerance = 70
        
        print "opening camera"
        self.feed = camFeed.CamFeed()
        
        print "opening PMD"
        self.depth = PMDReceiver.PMDReceiver()
        
        self.cameraMaxHorzAngle = 83.14 # calculated value, 90 is published
        self.cameraMaxVertAngle = 66    # calculated value, 90 is published
        self.depthMaxHorzAngle = 64     # calculated value, 66 is published value
        self.depthMaxVertAngle = 82
        self.separation = 0.04242      #distance between cameras
        print "Starting feed display"
        self.depthArray = self.depth.getImage()
        self.depthArray1 = self.depth.getImage()
        self.depthArray2 = self.depth.getImage()
        self.depthArray3 = self.depth.getImage()
#        A = numpy.zeros(self.depthArray.shape[:2])
        self.loops = 0
        self.successHistory = 0
        self.mid50SuccessHistory = 0
        self.mid25SuccessHistory = 0

#depthimagefile = 0;

    def correlate(self):
        
        self.loops+=1
            
        self.depthArray = self.depth.getImage()
        left = self.feed.getImage(1)
        right = self.feed.getImage(2)
        
    #    left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    #    right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
        
        self.depthArray4 = self.depthArray3
        self.depthArray3 = self.depthArray2
        self.depthArray2 = self.depthArray1
        self.depthArray1 = self.depthArray
        
        self.depthArray = (self.depthArray1*4+self.depthArray2*3+self.depthArray3*2+self.depthArray4)/10
        
    #    self.depthArray = cv2.fromarray(self.depthArray)
    #    self.depthArray = cv2.medianBlur(self.depthArray,3)
        
        cv2.imshow('DepthImage', self.depthArray)
        cv2.imshow('Left', left)
        cv2.imshow('Right', right)
        
        
        webcamRows, webcamColumns = left.shape[:2]    
    #    leftCenterline = left[math.floor(h/2)]
        
        h, w = right.shape[:2]
    #    rightCenterline = right[math.floor(h/2)]
        
        hArray, wArray = self.depthArray.shape[:2]    
    #    dAcenterline = self.depthArray[math.floor(h1/2)]
        
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
        self.leftInverseMap = numpy.zeros((webcamRows,webcamColumns,1))
        self.rightInverseMap = numpy.zeros((webcamRows,webcamColumns,1))
    
        errors = numpy.zeros((hArray,wArray),dtype=int)
        
        compArray = numpy.zeros((2,hArray,wArray,3), dtype=numpy.uint8)
        midCompArray = numpy.zeros((2,hArray/2,wArray/2))
        col=-1
        for r in range(0,hArray):         
            VertAngle = int((float(r)/float(hArray))*float(self.depthMaxVertAngle) + (float(self.cameraMaxVertAngle)-float(self.depthMaxVertAngle))/float(2))
            lWebcamYValue = int(float(webcamRows)*float(VertAngle)/float(self.cameraMaxVertAngle))
            rWebcamYValue = webcamRows*VertAngle/self.cameraMaxVertAngle
                    
            for c in range(0,wArray): 
                y = self.depthArray[r,c]   
                
                A = ((float(c)/wArray)*self.depthMaxHorzAngle)-(self.depthMaxHorzAngle/2)
               
    #                x=y*math.cos(math.radians(A))
                x = y
                C = A + 90      
                wL = math.sqrt(math.pow(x,2)+math.pow(self.separation,2) - 2*x*self.separation*math.cos(math.radians(C)))
                FL = math.degrees(math.asin(self.separation*math.sin(math.radians(C))/wL))
                DL = 180 - FL -C
                BL = 90 - DL
                lWebcamXValue = (BL + 45)*webcamColumns/self.cameraMaxHorzAngle
    
                if (lWebcamXValue < webcamColumns) and (lWebcamXValue>=0) and rWebcamYValue>=0 and rWebcamYValue<webcamRows:
                    leftMap[r,c,0] = lWebcamYValue
                    leftMap[r,c,1] = lWebcamXValue
                    compArray[0,r,c,:] = left[lWebcamYValue,lWebcamXValue,:]
                    self.leftInverseMap[lWebcamYValue,lWebcamXValue] = x
    #                
    #                    midCompArray[0,r-hArray/4,c-wArray/4] = left[lWebcamYValue,lWebcamXValue]
                        
                E = 180 - C
                wR = math.sqrt(math.pow(x,2)+math.pow(self.separation,2) - 2*x*self.separation*math.cos(math.radians(E)))
                FR = math.degrees(math.asin(self.separation*math.sin(math.radians(E))/wR))
                DR = 180 - FL - E
                BR = DR - 90
                rWebcamXValue = (BR + 45)*webcamColumns/self.cameraMaxHorzAngle
                if rWebcamXValue < w and rWebcamXValue>=0 and rWebcamYValue>=0 and rWebcamYValue<h:
                    rightMap[r,c,0] = rWebcamYValue
                    rightMap[r,c,1] = rWebcamXValue
                    compArray[1,r,c, :] = right[rWebcamYValue,rWebcamXValue, :]
                    self.rightInverseMap[rWebcamYValue,rWebcamXValue] = x
                    
    #            if abs(compArray[0,r,c]-compArray[1,r,c]<self.tolerance):
    #                success+=1
    #                if (r>hArray/4)and(r<hArray*3/4)and(c>wArray/4)and(c<wArray*3/4):
    #                    middle50Success+=1
    #                if (r>3*hArray/8)and(r<hArray*5/8)and(c>wArray*3/8)and(c<wArray*5/8):
    #                    middle25Success+=1
    #            else:
    #                errors[r,c]=255;
    #                    
    #    print self.loops
    #    successRate = float(success)/(hArray*wArray)
    #    print successRate
    #    mid50SuccessRate = float(middle50Success)/((hArray*wArray)/4)
    #    print mid50SuccessRate
    #    mid25SuccessRate = float(middle25Success)/((hArray*wArray)/16)
    #    print mid25SuccessRate
    #    self.successHistory = float(successRate+(self.successHistory*(self.loops-1)))/self.loops
    #    print self.successHistory
    #    self.mid50SuccessHistory = float(mid50SuccessRate+(self.mid50SuccessHistory*(self.loops-1)))/self.loops
    #    print self.mid50SuccessHistory
    #    self.mid25SuccessHistory = float(mid25SuccessRate+(self.mid25SuccessHistory*(self.loops-1)))/self.loops
    #    print self.mid25SuccessHistory
    #    
    #    dualMap = ((compArray[1,:,:])+(compArray[0,:,:]))/2
    #    dualMap = cv2.cvtColor(dualMap,cv2.COLOR_GRAY2BGR)
    #    errLoc = numpy.where(errors==255)
    #    for r in range(0,hArray):
    #        for c in range(0,wArray): 
    #            if errors[r,c]==255:
    #                dualMap[r,c,:]=[0,0,255];    
    #    
            compLResize = cv2.resize(compArray[0,:,:,:], None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
            compRResize = cv2.resize(compArray[1,:,:,:], None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
            
            cv2.imshow('CompareL', compLResize)    
            cv2.imshow('CompareR', compRResize)  
        
            compAvg = compLResize/2+compRResize/2
            
            compAvg = cv2.resize(compAvg, None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
            cv2.imshow('Average Of Correlation', compAvg)    
            
            
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break
    #        depthimagefile+=1;
    #        scaler = 255
    #        self.depthArray = self.depthArray*scaler
    #        filename = 'C:/ADEV/WinPython-64bit-2.7.10.3/python-2.7.10.amd64/Scripts/ADEV/depthImages/' + str(depthimagefile) + '.tiff'
    #        cv2.imwrite(filename, self.depthArray)
    #  
    #       
    #           
    #       
    #  
    def closeWindows(self):
            cv2.destroyWindow("Left")
            cv2.destroyWindow("Right")
            cv2.destroyWindow('DepthImage')
    
    #    for(pixel in self.depthArray):
    #        pixel = 
    #       A = ((xvalue/depth.getCols())*self.depthMaxHorzAngle)-90
    #       #if distance values aren't along the hypotenuse add next line
    #       #x = pixel*cos()
    #       #otherwise
    #       x=pixel
    #    
    #       # for left webcam
    #       if(A>0):
    #           C=A+90
    #       else:
    #           C = 90-A
    #       w = sqrt(x^2+self.separation^2 - 2*x*self.separation*cos(C)) # add some correction for C>90
    #       D = arcsin(x*sin(C)/w)
    #       B = 90 - D
    #       lWebcamXValue = B+90*webcamColumns/self.depthMaxHorzAngle
    #       #this is wrong, but close, need to throw in a factor for max vertical angle
    #       lWebcamYValue = (yvalue/depthRows)*webcamRows
        
    def getDistance(self, x, y, isLeft):
        # TODO: Change these values based on where origin of coordinate system 
        # should be. Currently centered on PMD lens
        if(isLeft):
            dxMod = -self.separation 
        else:
            dxMod = self.separation
        dyMod = 0
        dzMod = 0
        
        if(isLeft): 
            d = self.privateGetDistance(x,y,self.leftInverseMap)
            maxX, maxY = self.feed.getImage(1).shape[:2]
        else:
            d =  self.privateGetDistance(x,y,self.rightInverseMap)
            maxX, maxY = self.feed.getImage(2).shape[:2]
        maxX = float(maxX)
        maxY = float(maxY)
        x = float(x)
        y = float(y)
        A = float(self.cameraMaxHorzAngle)
        B = A*x/maxX
        C = B-A/2
        D = float(self.cameraMaxVertAngle)
        E = D*y/maxY
        F = D/2-E
        dx = d*math.sin(C)+dxMod
        dy = d*math.cos(C)+dyMod
        dz = d*math.sin(F)+dzMod
        return [dx, dy, dz, d]
        
                
                
            
    def privateGetDistance(self, x, y, inverseMap):
        if inverseMap(x,y)!=0:
            return inverseMap(x,y)
        else:
            return pixelSearch(x,y,1,inverseMap)
            
    def pixelSearch(self,x,y,r,inverseMap):
        numValues = int(0)
        sumValues = float(0)
        for xval in range(x-r,x+r):
            if inverseMap(xval,y-r)>0:
                numvalues+=1;
                sumValues+=inverseMap(xval,y-r)
            if inverseMap(xval,y+r)>0:
                numvalues+=1;
                sumValues+=inverseMap(xval,y+r)
        for yval in range(y-r,y+r):
            if inverseMap(x-r,yval)>0:
                numvalues+=1;
                sumValues+=inverseMap(x-r,yval)
            if inverseMap(x+r,yval)>0:
                numvalues+=1;
                sumValues+=inverseMap(x+r,yval)
        if numvalues>0:
            return sumvalues/numvalues
        else:
            return pixelSearch(x,y,r+1,inverseMap)
                
    
