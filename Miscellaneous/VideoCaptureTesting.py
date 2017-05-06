#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testing.py
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
#import antigravity
import time

from array import array
from socket import *
import sys
import select

address = ('localhost', 12345)
server_socket = socket(AF_INET, SOCK_DGRAM)
server_socket.bind(address)

rows = 120
cols = 176
numpix = rows*cols

count1 = 0
count2 = 0
fileName1 = "image1"
fileName2 = "image2"

K = np.array([[221.36336647, 0, 152.0058037], [0, 220.07218505, 105.41377619], [0, 0, 1]])
d = np.array([-0.37843677, 0.1629267, 0, 0, 0]) # just use first two terms (no translation)



cv2.namedWindow("preview1")
cv2.namedWindow("preview2")
vc1 = cv2.VideoCapture(1)
vc2 = cv2.VideoCapture(2)

if vc1.isOpened(): # try to get the first frame
    rval1, frame1 = vc1.read()
    pixels1 = frame1.data
else:
    rval1 = False

if vc2.isOpened(): # try to get the first frame
    rval2, frame2 = vc2.read()
    pixels2 = frame2.data
else:
    rval2 = False

#for i in range(0,frame1.rows):
#	for j in range(0,frame1.cols):
#	
#		b1 = pixels1[frame1.step * j + i] ;
#		g1 = pixels1[frame1.step * j + i + 1];
#		r1 = pixels1[frame1.step * j + i + 2];
#		
#	
#for i in range(0,frame2.rows):
#	for j in range(0,frame2.cols):
#		
#		b2 = pixels2[frame2.step * j + i] ;
#		g2 = pixels2[frame2.step * j + i + 1];
#		r2 = pixels2[frame2.step * j + i + 2];

while rval1 & rval2:
	#code to store frame as an unique image here
#    time.sleep(1)#3s time delay
#    if count1<200:
#        count1 = count1+1
    newImage1 = np.copy(frame1);
    tempfileName1 = fileName1+".jpg" #+ str(count1) + ".jpg"
    cv2.imwrite(tempfileName1, newImage1)
    #    if count2<100:
    #        count2 = count1+1
    #        newImage2 = np.copy(frame2);
    #        tempfileName2 = fileName2 + str(count2) + ".png"
    #        cv2.imwrite(tempfileName2, newImage2)
    img = cv2.imread(fileName1+".jpg")  
    # read one of your images
    h1, w1 = img.shape[:2]
#    h2, w2 = newImage2.shape[:2]
    
    

    # undistort
    newcamera1, roi = cv2.getOptimalNewCameraMatrix(K, d, (w1,h1), 0) 
    newImageUndist1 = cv2.undistort(img, K, d, None, newcamera1)
        
#    newcamera2, roi = cv2.getOptimalNewCameraMatrix(K, d, (w2,h2), 0) 
#    newImage2 = cv2.undistort(newImage2, K, d, None, newcamera2)
#        
        
    cv2.imshow("preview1",frame1)
    rval1, frame1 = vc1.read()
    cv2.imshow("preview2",frame2)
    rval2, frame2 = vc2.read()
    
    recv1, addr = server_socket.recvfrom(65536)
    recv2, addr = server_socket.recvfrom(65536)
    if recv1[0] == 1:        
        recv = recv1 + recv2
    elif recv2[0] == 2:
        recv = recv1 + recv2
    elif recv1[0] == 2:
        recv = recv2 + recv1            
    else:
        recv = recv2 + recv1
    fImg = array('f', recv)
    
    img = np.reshape(fImg, (-1, cols))
    
    	# Display
    cv2.imshow('DepthImage', img)
    key = cv2.waitKey(20)	#every 20 ms, checks if a key has been pressed.
    if key == 27: # exit on ESC
        break
    
	
		
	
    
cv2.destroyWindow("preview1")
cv2.destroyWindow("preview2")
cv2.destroyWindow('DepthImage')


