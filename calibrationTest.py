# -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 15:25:25 2016

@author: georgedr
"""

import numpy as np
import cv2


cv2.namedWindow("preview1")
cv2.namedWindow("preview2")



# copy parameters to arrays
K = np.array([[221.36336647, 0, 152.0058037], [0, 220.07218505, 105.41377619], [0, 0, 1]])
d = np.array([-0.37843677, 0.1629267, 0, 0, 0]) # just use first two terms (no translation)

# read one of your images
img = cv2.imread("C:/ADEV/calibration images/Webcam1/wc1-0 (2).JPG")
h, w = img.shape[:2]

# undistort
newcamera, roi = cv2.getOptimalNewCameraMatrix(K, d, (w,h), 0) 
newimg = cv2.undistort(img, K, d, None, newcamera)

#cv2.imwrite("original.jpg", img)
#cv2.imwrite("undistorted.jpg", newimg)

while True:
    cv2.imshow("preview1",img)
    cv2.imshow("preview2",newimg)
    if cv2.waitKey(1) == 27:
        break #esc to quit

    
	
		
	
    
cv2.destroyWindow("preview1")
cv2.destroyWindow("preview2")

