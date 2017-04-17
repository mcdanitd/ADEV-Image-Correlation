
import cv2
import numpy as np
#import antigravity
import time

fileName1 = "image1"
fileName2 = "image2"



cv2.namedWindow("preview")
vc1 = cv2.VideoCapture(0)

if vc1.isOpened(): # try to get the first frame
    rval1, frame1 = vc1.read()
    pixels1 = frame1.data
else:
    rval1 = False


while rval1:
	#code to store frame as an unique image here
    newImage1 = np.copy(frame1);
    tempfileName1 = fileName1+".jpg"
    cv2.imwrite(tempfileName1, newImage1)
    #code to store information in a .txt file
    f= open("Information.txt","w+")
    f.write("Date and time")
    f.write("\n")
    #run a loop to write a line for each distinct strawberry
    f.write("Strawberry at coordinates")
    f.write("\n")
    
    img = cv2.imread(fileName1+".jpg")  
    # read new image
        
    cv2.imshow("preview",img)
    rval, frame = vc1.read()
    key = cv2.waitKey(20)	#every 20 ms, checks if a key has been pressed.
    if key == 27: # exit on ESC
        break
    
	
		
	
    
cv2.destroyWindow("preview")
