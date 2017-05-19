#Reads input from both webcams. Outputs current camera images when prompted

import cv2
import numpy as np
#import antigravity
import time

from array import array
from socket import *
import sys
import select

class CamFeed:
    

    def __init__(self):
        self.vc1 = cv2.VideoCapture(1)
        self.vc2 = cv2.VideoCapture(2)
        
        #Webcam Distortion Calibration, use Calibration.py to create a calibFile for each camera.
        calibFile = np.load('calibFile.npz')
        self.mtx = calibFile['arr_0']
        self.dist = calibFile['arr_1']
        self.newcameramtx = calibFile['arr_2']
        self.roi = calibFile['arr_3']
        self.x,self.y,self.w,self.h = self.roi
        
        
        while (not (self.camsOpen())):
            pass
    
    #Starts both cameras
    def camsOpen(self):
        if self.vc1.isOpened(): # try to get the first frame
            rval1, frame1 = self.vc1.read()
        else:
            rval1 = False
        
        if self.vc2.isOpened(): # try to get the first frame
            rval2, frame2 = self.vc2.read()
        else:
            rval2 = False

        
        return rval1+rval2
            
    #Returns the current image from a camera
    def getImage(self, cam):
        if cam==1:
        	rval, frame = self.vc1.read() 
            
        else:
            rval, frame = self.vc2.read()
                 
        # rotate images.  Cameras are placed upside-down in the mount.
        frame = cv2.undistort(frame, self.mtx, self.dist, None, self.newcameramtx)
        frame = frame[self.y:self.y+self.h, self.x:self.x+self.w]
        h, w = frame.shape[:2]
        M = cv2.getRotationMatrix2D((w/2,h/2),180,1)    
        frame = cv2.warpAffine(frame,M,(w,h))
        return frame
     
