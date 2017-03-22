# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:27:37 2017

@author: georgedr
"""

import Correlator
import cv2
from Tkinter import *
from PIL import Image, ImageTk

global leftLabel
global rightLabel
global depthLabel

global distancesLabelFrame
global dLabel
global dxLabel
global dyLabel
global dzLabel

global bottomBar

global corr

def update():
    [depth, left, right] = corr.correlate()
    
    left = cv2.cvtColor(left, cv2.COLOR_BGR2RGB)
    leftImage = Image.fromarray(left)  
    leftPhoto = ImageTk.PhotoImage(leftImage)
    leftLabel.configure(image=leftPhoto)
    leftLabel.image = leftPhoto
    
    right = cv2.cvtColor(right, cv2.COLOR_BGR2RGB)
    rightImage = Image.fromarray(right)
    rightPhoto = ImageTk.PhotoImage(rightImage)
    rightLabel.configure(image=rightPhoto)
    rightLabel.image = rightPhoto
    
#    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
#    depthImage = Image.fromarray(depth)
#    depthPhoto = ImageTk.PhotoImage(depthImage)
#    depthLabel.configure(image=depthPhoto)
#    depthLabel.image = depthPhoto
	
    master.after(1000/30, update)
    

        
def leftCameraClick(event):
    [dx, dy, dz, d] = corr.getDistance(event.x, event.y, True)
#   do stuff to display/highlight clicked area on other images
    [depth, left, right] = corr.correlate()
    
#    right = cv2.circle(right, rightCoor, 25, Scalar(0,255,255,100))
    right = cv2.cvtColor(right, cv2.COLOR_BGR2RGB) 
    rightImage = Image.fromarray(right)
    rightPhoto = ImageTk.PhotoImage(rightImage)
    rightLabel.configure(image=rightPhoto)
    rightLabel.image = rightPhoto
    
#    depth = cv2.circle(depth, depthCoor, 25, Scalar(0,255,255,100))
#    depth = cv2.cvtColor(depth, cv2.COLOR_BGR2RGB)
#    depthImage = Image.fromarray(depth)
#    depthPhoto = ImageTk.PhotoImage(depthImage)
#    depthLabel.configure(image=depthPhoto)
#    depthLabel.image = depthPhoto
    
    dxString = "dx:  " + str(dx)
    dxLabel.configure(text = dxString)
    
    dyString = "dy:  " + str(dy)
    dyLabel.configure(text = dyString)
    
    dzString = "dz:  " + str(dz)
    dzLabel.configure(text = dzString)
    
    dString = "d:  " + str(d)
    dLabel.configure(text = dString)
    
    bbString = "Left X: " + str(event.x) + "  Y: " + str(event.y)
    bottomBar.configure(text = bbString)
    
    
    
def rightCameraClick(event):
    [dx, dy, dz, d] = corr.getDistance(event.x, event.y, False)
    
    
	
    
    
corr = Correlator.Correlator()
[depth, left, right] = corr.correlate()


master = Tk()

leftLabel = Label(master)
leftLabel.grid(row=0, column=0)

rightLabel = Label(master, text="image go here")
rightLabel.grid(row=0, column=1)

depthLabel = Label(master, text="image go here")
depthLabel.grid(row=1, column=1)

distancesLabelFrame = LabelFrame(master, width = 400, height = 500)
distancesLabelFrame.grid(row = 1, column = 0)


dxLabel = Label(distancesLabelFrame, text = "dx:", anchor = W)
dxLabel.pack()

dyLabel = Label(distancesLabelFrame, text = "dy:", anchor = W)
dyLabel.pack()

dzLabel = Label(distancesLabelFrame, text = "dz:", anchor = W)
dzLabel.pack()

dLabel = Label(distancesLabelFrame, text = "d:", anchor = W)
dLabel.pack()




bottomBar = Label(master, justify=LEFT, anchor = W)
bottomBar.grid(row=3)



#mouseclick event
leftLabel.bind("<Button 1>",leftCameraClick)
rightLabel.bind("<Button 1>",rightCameraClick)

print "about to update"


master.after(1000, update)
mainloop()

