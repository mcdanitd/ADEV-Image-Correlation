#CorrelationApp.py

# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 12:53:34 2017

@author: georgedr
"""

import Correlator
import cv2

corr = Correlator.Correlator()

def leftWindowClick(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:   
          [dx, dy, dz, d] = corr.getDistance(x, y, True)  
          print("dx: " + dx[0].astype('str') + "\ndy: " + dy[0].astype('str') + "\ndz: " + dz[0].astype('str') + "\nStraightLineDistance: " + d[0].astype('str'))
		
  
  
def rightWindowClick(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN: 
        [dx, dy, dz, d] = corr.getDistance(x, y, False)
        print("dx: " + dx[0].astype('str') + "\ndy: " + dy[0].astype('str') + "\ndz: " + dz[0].astype('str') + "\nStraightLineDistance: " + d[0].astype('str'))
    
    
cv2.namedWindow("left")
cv2.setMouseCallback("left", leftWindowClick)
cv2.namedWindow("right")
cv2.setMouseCallback("right", rightWindowClick)

while True:
    
    [depth, left, right] = corr.correlate()
    
    cv2.imshow("left", left)
    cv2.imshow("right", right)
    cv2.imshow("depth", depth)   
    
    
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
    
cv2.destroyWindow("left")
cv2.destroyWindow("right")
cv2.destroyWindow("depth")
corr.closeWindows()