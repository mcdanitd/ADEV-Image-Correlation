# ADEV Image Correlation
# 6 Feburary 2017

# GUI testing script.  We want to display a webcam's input and be able to know the coordinates of a user click.


import cv2
#import antigravity

def click(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		output = "X Location: " + repr(x) + "  Y Location: " + repr(y)
		print(output)

cv2.namedWindow("preview")
cv2.setMouseCallback("preview", click)
vc = cv2.VideoCapture(1)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

while rval:
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    if key == 27: # exit on ESC
        break
cv2.destroyWindow("preview")
