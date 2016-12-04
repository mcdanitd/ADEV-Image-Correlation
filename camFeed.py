#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  camFeed.py
#  
#  Copyright 2016 mcdanitd <mcdanitd@MCDANITD-1>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import cv2
import numpy as np
#import antigravity # fun easter egg in python
import time

from array import array
from socket import *
import sys
import select

class CamFeed:
    
#    self.size = []
        
    # distortion removal matrices
    #K = np.array([[221.36336647, 0, 152.0058037], [0, 220.07218505, 105.41377619], [0, 0, 1]])
    #d = np.array([-0.37843677, 0.1629267, 0, 0, 0]) # just use first two terms (no translation)
    def __init__(self):
#        cv2.namedWindow("preview1")
#        cv2.namedWindow("preview2")
        self.vc1 = cv2.VideoCapture(1)
        self.vc2 = cv2.VideoCapture(2)
        while (not (self.camsOpen())):
            pass
    
    def camsOpen(self):
        if self.vc1.isOpened(): # try to get the first frame
            rval1, frame1 = self.vc1.read()
        else:
            rval1 = False
        
        if self.vc2.isOpened(): # try to get the first frame
            rval2, frame2 = self.vc2.read()
        else:
            rval2 = False
#        
#        if (!rval2):
#            
#            && (rval1 == True)):
#            return True
        
        return rval1+rval2
            
    def getImage(self, cam):
        if cam==1:
        	rval, frame = self.vc1.read() 
            
        else:
            rval, frame = self.vc2.read()
        h, w = frame.shape[:2]
            
        #  
            # undistort the image
        #    newcamera1, roi = cv2.getOptimalNewCameraMatrix(K, d, (w1,h1), 0) 
        #    newImageUndist1 = cv2.undistort(img, K, d, None, newcamera1)
                
        #    newcamera2, roi = cv2.getOptimalNewCameraMatrix(K, d, (w2,h2), 0) 
        #    newImage2 = cv2.undistort(newImage2, K, d, None, newcamera2)
        #       
            # rotate images so they look right
        M = cv2.getRotationMatrix2D((w/2,h/2),180,1)    
        frame = cv2.warpAffine(frame,M,(w,h))
            
             # display the image to the windows   
#        cv2.imshow("preview1",frame)
        return frame
     
       
#        key = cv2.waitKey(20)	#every 20 ms, checks if a key has been pressed.
#        if key == 27: # exit on ESC
#            break
#        
#    	
#    		
#    	
#        
#    cv2.destroyWindow("preview1")
#    cv2.destroyWindow("preview2")
#    cv2.destroyWindow('DepthImage')
#    
#    
