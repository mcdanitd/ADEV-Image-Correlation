# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:27:37 2017

@author: georgedr
"""

import Correlator
import cv2
from Tkinter import *
from PIL import Image, ImageTk
import numpy as np

global leftLabel
global rightLabel
global depthLabel

global distancesLabelFrame
global dLabel
global dxLabel
global dyLabel
global dzLabel
global dEntry
global dxEntry
global dyEntry
global dzEntry
global testButton
global testDiff
global testDiffx
global testDiffy
global testDiffz
global testDiffPercent

global d
global dx
global dy
global dz

d=0
dx=0
dy=0
dz=0

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
    depthImage = Image.fromarray(depth * 255 / np.amax(depth))
    depthPhoto = ImageTk.PhotoImage(depthImage)
    depthLabel.configure(image=depthPhoto)
    depthLabel.image = depthPhoto
	
    master.after(1000/30, update)
    

        
def leftCameraClick(event):
    global d
    global dx
    global dy
    global dz
    [dx, dy, dz, d] = corr.getDistance(event.x, event.y, True)
    dx = dx[0]
    dy = dy[0]
    dz = dz[0]
    d  = d[0]
#   do stuff to display/highlight clicked area on other images
    [depth, left, right] = corr.correlate()
    
#    right = cv2.circle(right, rightCoor, 25, Scalar(0,255,255,100))
    right = cv2.cvtColor(right, cv2.COLOR_BGR2RGB) 
    rightImage = Image.fromarray(right)
    rightPhoto = ImageTk.PhotoImage(rightImage)
    rightLabel.configure(image=rightPhoto)
    rightLabel.image = rightPhoto
    
#    depth = cv2.circle(depth, depthCoor, 25, Scalar(0,255,255,100))
#    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
#    depthImage = Image.fromarray(depth)
#    depthPhoto = ImageTk.PhotoImage(depthImage)
#    depthLabel.configure(image=depthPhoto)
#    depthLabel.image = depthPhoto
    
    dxString = "dx:  " + "%.3f" % dx
    dxLabel.configure(text = dxString)
    
    dyString = "dy:  " + "%.3f" % dy
    dyLabel.configure(text = dyString)
    
    dzString = "dz:  " + "%.3f" % dz
    dzLabel.configure(text = dzString)
    
    dString = "d:  " + "%.3f" % d
    dLabel.configure(text = dString)
    
    bbString = "Left X: " + str(event.x) + "  Y: " + str(event.y)
    bottomBar.configure(text = bbString)
    
    
    
def rightCameraClick(event): #TODO add over from left camera
    global d
    global dx
    global dy
    global dz
    [dx, dy, dz, d] = corr.getDistance(event.x, event.y, False)
    dx = dx[0]
    dy = dy[0]
    dz = dz[0]
    d  = d[0]
#   do stuff to display/highlight clicked area on other images
    [depth, left, right] = corr.correlate()
    
#    right = cv2.circle(right, rightCoor, 25, Scalar(0,255,255,100))
#    right = cv2.cvtColor(right, cv2.COLOR_BGR2RGB) 
#    rightImage = Image.fromarray(right)
#    rightPhoto = ImageTk.PhotoImage(rightImage)
#    rightLabel.configure(image=rightPhoto)
#    rightLabel.image = rightPhoto
    
#    depth = cv2.circle(depth, depthCoor, 25, Scalar(0,255,255,100))
#    depth = cv2.cvtColor(depth, cv2.COLOR_GRAY2RGB)
#    depthImage = Image.fromarray(depth)
#    depthPhoto = ImageTk.PhotoImage(depthImage)
#    depthLabel.configure(image=depthPhoto)
#    depthLabel.image = depthPhoto
    
    dxString = "dx:  " + "%.3f" % dx
    dxLabel.configure(text = dxString)
    
    dyString = "dy:  " + "%.3f" % dy
    dyLabel.configure(text = dyString)
    
    dzString = "dz:  " + "%.3f" % dz
    dzLabel.configure(text = dzString)
    
    dString = "d:  " + "%.3f" % d
    dLabel.configure(text = dString)
    
    bbString = "Right X: " + str(event.x) + "  Y: " + str(event.y)
    bottomBar.configure(text = bbString)
    
 
def checkAccuracy():
    global d
    global dx
    global dy
    global dz
    
    dxString = "diffx:  " + "%.3f" % (dx - float(dxEntry.get()))
    testDiffx.configure(text = dxString)
    
    dyString = "diffy:  " + "%.3f" % (dy - float(dyEntry.get()))
    testDiffy.configure(text = dyString)
    
    dzString = "diffz:  " + "%.3f" % (dz - float(dzEntry.get()))
    testDiffz.configure(text = dzString)
    
    dString = "diff:  " + "%.3f" % (d - float(dEntry.get()))
    testDiff.configure(text = dString)
    
    
    
	
    
    
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


dxLabel = Label(distancesLabelFrame, text = "dx:")
dxLabel.grid(row=0, column=0)

dyLabel = Label(distancesLabelFrame, text = "dy:")
dyLabel.grid(row=1, column=0)

dzLabel = Label(distancesLabelFrame, text = "dz:")
dzLabel.grid(row=2, column=0)

dLabel = Label(distancesLabelFrame, text = "d:")
dLabel.grid(row=3, column=0)

dxEntry = Entry(distancesLabelFrame, text = "dx:")
dxEntry.grid(row=0, column=1)

dyEntry = Entry(distancesLabelFrame, text = "dy:")
dyEntry.grid(row=1, column=1)

dzEntry = Entry(distancesLabelFrame, text = "dz:")
dzEntry.grid(row=2, column=1)

dEntry = Entry(distancesLabelFrame, text = "d:")
dEntry.grid(row=3, column=1)

testButton = Button(distancesLabelFrame, text = "Check Accuracy", command = checkAccuracy)
testButton.grid(row=4, column=1)

testDiffx = Label(distancesLabelFrame, text = "DiffX")
testDiffx.grid(row=0, column=2)

testDiffy = Label(distancesLabelFrame, text = "DiffY")
testDiffy.grid(row=1, column=2)

testDiffz = Label(distancesLabelFrame, text = "DiffZ")
testDiffz.grid(row=2, column=2)

testDiff = Label(distancesLabelFrame, text = "Diff")
testDiff.grid(row=3, column=2)

#testDiffPercent = Label(distancesLabelFrame, text = "DiffPercent")
#testDiffPercent.grid(row=4, column=2)


bottomBar = Label(master)
bottomBar.grid(row=2)



#mouseclick event
leftLabel.bind("<Button 1>",leftCameraClick)
rightLabel.bind("<Button 1>",rightCameraClick)

print "about to update"


master.after(1000, update)
mainloop()

