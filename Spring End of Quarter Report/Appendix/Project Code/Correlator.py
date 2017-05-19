import PMDReceiver
import camFeed
import cv2
import math
import numpy
import time
import numpy as np
import ConfigParser


class Correlator:
    
    def __init__(self):
        
        self.tolerance = 70
        
        print "opening camera"
        self.feed = camFeed.CamFeed()
        
        print "opening PMD"
        self.depth = PMDReceiver.PMDReceiver()
        #TODO: adjust these values to reflect physical values
        self.cameraMaxHorzAngle = 83    # calculated value, 90 is published
        self.cameraMaxVertAngle = 66    # calculated value, 90 is published
        self.depthMaxHorzAngle = 64     # calculated value, 66 is published value
        self.depthMaxVertAngle = 82
#        self.separation = 0.0437       # values measured 5/6/2017
#        self.separation = 0.0452       # values measured 5/6/2017
        self.separation = 0.04242       #distance between webcam and depth camera in meters
        print "Starting feed display"
        
        # initializing depthArrays for 
        self.depthArray = self.depth.getImage()
        self.depthArray1 = self.depth.getImage()
        self.depthArray2 = self.depth.getImage()
        self.depthArray3 = self.depth.getImage()
        
        
        #info for cropping images to have identical input from web cameras
        #TODO: modify settings.ini for your web cameras
        Config = ConfigParser.ConfigParser()
        Config.read("settings.ini")
        
        self.minYLeft = Config.getint("SectionOne", "minYLeft")
        self.maxYLeft = Config.getint("SectionOne", "maxYLeft") 
        self.minXLeft = Config.getint("SectionOne", "minXLeft")
        self.maxXLeft = Config.getint("SectionOne", "maxXLeft")
        
        self.minYRight = Config.getint("SectionOne", "minYRight")
        self.maxYRight = Config.getint("SectionOne", "maxYRight") 
        self.minXRight = Config.getint("SectionOne", "minXRight")
        self.maxXRight = Config.getint("SectionOne", "maxXRight")
        
               

    def correlate(self):       
            
        self.depthArray = self.depth.getImage()
        left = self.feed.getImage(1)
        right = self.feed.getImage(2)
        
        # cropping images with info from settings.ini file
        left = left[self.minYLeft:self.maxYLeft, self.minXLeft:self.maxXLeft]
        right = right[self.minYRight:self.maxYRight, self.minXRight:self.maxXRight]
        
        # shifting depth arrays for time averaging
        self.depthArray4 = self.depthArray3
        self.depthArray3 = self.depthArray2
        self.depthArray2 = self.depthArray1
        self.depthArray1 = self.depthArray
        
        #TODO: some options for averaging depth array
#        self.depthArray = (self.depthArray1*4+self.depthArray2*3+self.depthArray3*2+self.depthArray4)/10        
        self.depthArray = (self.depthArray1*2+self.depthArray2)/3
        
        # displays undistorted and cropped webcam feeds and averaged depth feed
        # these are the images used for correlation.
#        cv2.imshow('DepthImage', self.depthArray)
#        cv2.imshow('Left', left)
#        cv2.imshow('Right', right)
        
        # getting sizes of webcam image and depth array
        webcamRows, webcamColumns = left.shape[:2]            
        hArray, wArray = self.depthArray.shape[:2]    
        
        # these are the arrays that are the size of the depthcam
        # corresponding pixel, ie. (x, y), from webcams will be mapped onto them.
        leftMap = numpy.zeros((hArray,wArray,2))
        rightMap = numpy.zeros((hArray,wArray,2))
        
        # these are the arrays that are the same size as the webcams
        # corresponding depth values will be mapped onto them 
        self.leftInverseMap = -1*numpy.ones((webcamRows,webcamColumns,1))
        self.rightInverseMap = -1*numpy.ones((webcamRows,webcamColumns,1))
    
        # 4-D array composed of two 3-D arrays.
        # These arrays have the height and width of the depthcam, with three color channels
        # correspond pixel data from each webcam is mapped onto these arrays.
        # compArray[0] is the left webcam mapped onto the depth array
        # compArray[1] is the right webcam mapped onto the depth array
        compArray = numpy.zeros((2,hArray,wArray,3), dtype=numpy.uint8)
    
        for r in range(0,hArray):         
            VertAngle = int((float(r)/float(hArray))*float(self.depthMaxVertAngle) + (float(self.cameraMaxVertAngle)-float(self.depthMaxVertAngle))/float(2))
            lWebcamYValue = int(float(webcamRows)*float(VertAngle)/float(self.cameraMaxVertAngle))
            rWebcamYValue = int(webcamRows*VertAngle/self.cameraMaxVertAngle)
                    
            for c in range(0,wArray): 
                x = self.depthArray[r,c] 
                
                # if the depth from the PMD is 0 (flagged as invalid), don't correlate
                if (x!=0):  
                    # Variables here are pretty arbitrarily named, refer to the diagram  ###
                    # TODO: make clean diagram of this and put file name here------------^.
                    A = ((float(c)/wArray)*self.depthMaxHorzAngle)-(self.depthMaxHorzAngle/2)                  
                    
                    C = A + 90      
                    wL = math.sqrt(math.pow(x,2)+math.pow(self.separation,2) - 2*x*self.separation*math.cos(math.radians(C)))
                    FL = math.degrees(math.asin(self.separation*math.sin(math.radians(C))/wL))
                    DL = 180 - FL -C
                    BL = 90 - DL
                    lWebcamXValue = int((BL + 45)*webcamColumns/self.cameraMaxHorzAngle)
        
                    if (lWebcamXValue < webcamColumns) and (lWebcamXValue>=0) and rWebcamYValue>=0 and rWebcamYValue<webcamRows:
                        leftMap[r,c,0] = lWebcamYValue
                        leftMap[r,c,1] = lWebcamXValue
                        compArray[0,r,c] = left[int(lWebcamYValue),int(lWebcamXValue),:]
                        self.leftInverseMap[int(lWebcamYValue),int(lWebcamXValue)] = x
                            
                    E = 180 - C
                    wR = math.sqrt(math.pow(x,2)+math.pow(self.separation,2) - 2*x*self.separation*math.cos(math.radians(E)))
                    FR = math.degrees(math.asin(self.separation*math.sin(math.radians(E))/wR))
                    DR = 180 - FL - E
                    BR = DR - 90
                    rWebcamXValue = int((BR + 45)*webcamColumns/self.cameraMaxHorzAngle)
                    if rWebcamXValue < w and rWebcamXValue>=0 and rWebcamYValue>=0 and rWebcamYValue<h:
                        rightMap[r,c,0] = rWebcamYValue
                        rightMap[r,c,1] = rWebcamXValue
                        compArray[1,r,c, :] = right[rWebcamYValue,rWebcamXValue, :]
                        self.rightInverseMap[rWebcamYValue,rWebcamXValue] = x
                
                          
        # expands the compArrays to make them easier to view 
        compLResize = cv2.resize(compArray[0,:,:,:], None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
        compRResize = cv2.resize(compArray[1,:,:,:], None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
        
        # displays the webcam image mapped onto the depth image
        cv2.imshow('CompareL', compLResize)    
        cv2.imshow('CompareR', compRResize)  
    
        # averages the left and right mapped onto the depth image, 
        # ideally would be identical, though this won't always be the case due to view angles.
#        compAvg = compLResize/2+compRResize/2
#        
#        compAvg = cv2.resize(compAvg, None,fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
#        cv2.imshow('Average Of Correlation', compAvg) 
        
        return [self.depthArray, left, right]
            

        """
        gets the distance to a point on a web camera
        @Parameters: int x - column of pixel to get distance of
                     int y - row of pixel to get distance of
                     boolean isLeft - indicates which camera the x and y value are from
        @Returns:
                float array in the form of [dx,dy,dz,d], please refer to documentation for image of coordinate system
        """
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
            
        # TODO: Similar to the meat of the correlate function, the variables here are hard to give 
        # meaningful names, refer to XXX.png to understand these variables.  
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
        dx = d*math.sin(math.radians(C))+dxMod
        dy = d*math.sin(math.radians(F))+dzMod
        dz = d*math.cos(math.radians(C))+dyMod        
        return [dx, dy, dz, d]
        
                
                
        """
        called by getDistance with the desired webcam;
        returns the distance of the desired pixel or calls for a search of the surrounding pixels
        """
    def privateGetDistance(self, x, y, inverseMap):
        if inverseMap[y,x]!= -1:
            return inverseMap[y,x]
        else:
            return self.pixelSearch(x,y,1,inverseMap)
            
        """
        used to recursively find the nearest pixel with an associated depth value by searching concentric squares. 
        (x,y) is the center of the search, r is the current radius (technically half side length) to search.
        """
    def pixelSearch(self,x,y,r,inverseMap):
        # TODO: look for ways to utilize edge detection to improve accuracy, might not be worth extra calculating time.
        # TODO: This searches using concentric squares as it was faster to get implemented and, 
        #       for smaller max radii, wouldn't be too different from concentric circles, in the 
        #       future, it might be wise to switch to a concentric circle searching algorithm.
        # TODO: the max search radius may need tweaking
        maxRadius = 20
        if(r>maxRadius):
            return np.zeros(1);
        yLimit, xLimit = inverseMap.shape[:2]        
        numValues = 0
        sumValues = 0.0
        
        # setting the bounds of the square to search,
        # if the square would go out of bounds of the image, 
        # the bounds of the square are set to the bounds of the image
        if y-r<0:
            ymin = 0
        else: 
            ymin = y-r
        if y+r>yLimit-1:
            ymax = yLimit-1
        else:
            ymax = y+r
        if x-r<0:
            xmin = 0
        else:
            xmin = x-r
        if x+r>xLimit-1:
            xmax = xLimit-1
        else:
            xmax = x+r
        
        # loops through the horizontal lines of the square
        for xval in range(xmin,xmax):            
            if inverseMap[ymin,xval]>=0:
                numValues+=1;
                sumValues+=inverseMap[ymin,xval]
                print(sumValues)
            if inverseMap[ymax,xval]>=0:
                numValues+=1;
                sumValues+=inverseMap[ymax,xval]
                print(sumValues)
        
        # loops through the vertical lines of the square
        for yval in range(ymin,ymax):
            if inverseMap[yval,xmin]>=0:
                numValues+=1;
                sumValues+=inverseMap[yval,xmin]
                print(sumValues)
            if inverseMap[yval,xmax]>=0:
                numValues+=1;
                sumValues+=inverseMap[yval,xmax]
                print(sumValues)
        
        # checks to see if a depth was found, 
        # if so, the average of the depths found is returned,
        # if not, a recursive call is made with an increased radius
        if numValues>0:
            print("\n")
            return sumValues/numValues
        else:
            return self.pixelSearch(x,y,r+1,inverseMap)
                
    
