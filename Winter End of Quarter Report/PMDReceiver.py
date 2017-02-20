# PMDReciever.py


import cv2
import numpy as np

from array import array
from socket import *

class PMDReceiver:
    def __init__(self):
        address = ('localhost', 12345)
        self.server_socket = socket(AF_INET, SOCK_DGRAM)
        self.server_socket.bind(address)
        
        self.rows = 120
        self.cols = 176
        self.numpix = self.rows*self.cols
        
    
    def getImage(self):
    	#120 * 176 = 21120 elements in array.
    	# Each element is 4 bytes in size.
    	# 21120 * 4 = 84480 byes total.
    	# Each UDP message can only carry 65536, so just
    	# split the image up over 2 messages.
        
        recv1, addr = self.server_socket.recvfrom(65536)
        recv2, addr = self.server_socket.recvfrom(65536)
        
#        recv = recv1 + recv2
        if recv1[0] == 1:        
            recv = recv1 + recv2
        elif recv2[0] == 2:
            recv = recv1 + recv2
        elif recv1[0] == 2:
            recv = recv2 + recv1            
        else:
            recv = recv2 + recv1
        
#        top = self.getTop()
#        bottom = self.getBottom()
#        recv = top + bottom
        fImg = array('f', recv)
        
        img = np.reshape(fImg, (-1, self.cols))
        img = np.rot90(img,1)
#        h1, w1 = img.shape[:2]
#        M = cv2.getRotationMatrix2D((w1/2,h1/2),90,1)
#        rotimg = np.zeros((w1,h1))
#        rotimg = cv2.warpAffine(img,M,(h1,w1))
        
        	# Display
#        cv2.imshow('DepthImage', img)
        return img
        
        
    def getTop(self):
        print "getting top"
        recv, addr = self.server_socket.recvfrom(65536)
        while recv[0]!= 1:
            recv, addr = self.server_socket.recvfrom(65536)
            print recv[1]
        return recv
    
        
    def getBottom(self):
        print "getting bot"
        recv, addr = self.server_socket.recvfrom(65536)
        while recv[0]!= 2:
            recv, addr = self.server_socket.recvfrom(65536)
        return recv
        
    def getSize(self):
        return [self.rows, self.cols]
        
    def getRows(self):
        return self.rows
        
    def getCols(self):
        return self.cols
        
    

