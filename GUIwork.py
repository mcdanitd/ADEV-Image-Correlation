# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 16:27:37 2017

@author: georgedr
"""
# This serves as the GUI for the correlator. This may be useful as a guide
# for demonstrating how the robot should interface with the correlation algorithm 


import Correlator
import cv2
from Tkinter import *
from PIL import Image, ImageTk
import numpy as np
import DataStorage

global leftLabel
global rightLabel
global depthLabel

global left
global right

global distancesLabelFrame
global dLabel
global dxLabel
global dyLabel
global dzLabel

global recordLeftButton
global recordRightButton

#global dEntry
#global dxEntry
#global dyEntry
#global dzEntry
#global testButton
#global testDiff
#global testDiffx
#global testDiffy
#global testDiffz
#global testDiffPercent

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

#Updates the webcam and depth camera images in the GUI
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
    
    depthImage = Image.fromarray(depth * 255 / np.amax(depth))
    depthPhoto = ImageTk.PhotoImage(depthImage)
    depthLabel.configure(image=depthPhoto)
    depthLabel.image = depthPhoto
	
    master.after(1000/30, update)
    

#Handles calculations for when the user clicks on the left camera's image
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
	#TODO: Add ability to Correlator.py - do stuff to display/highlight clicked area on other images
    [depth, left, right] = corr.correlate()

#	 for highlighting correspong pixel in right camera and depth camera, needs more data from corr.correlate before implementing
#	 clicking on left cameras image would highlight that object in the right camera's image
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
    
    bbString = "Left X: " + str(event.x) + "  Y: " + str(event.y)
    bottomBar.configure(text = bbString)
    
    
#Handles calculations for when the user clicks on the right camera's image
def rightCameraClick(event): #TODO: add over from left camera
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
    #[depth, left, right] = corr.correlate()

# same as in leftCameraClick
#	 clicking onright cameras image would highlight that object in the leftt camera's image
#    left = cv2.circle(left, leftCoor, 25, Scalar(0,255,255,100))
#    left = cv2.cvtColor(left, cv2.COLOR_BGR2RGB) 
#    leftImage = Image.fromarray(left)
#    leftPhoto = ImageTk.PhotoImage(leftImage)
#    leftLabel.configure(image=leftPhoto)
#    leftLabel.image = leftPhoto
    
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
    
#These two functions call a script to save the current image as a .png and some information on it as a .txt
def recordLeft():
    global left
    DataStorage.save(left, "Left")
    
def recordRight():
    global right
    DataStorage.save(right, "Right")

    
    #Uncomment to be able to check the correlation accuracy
#def checkAccuracy():
#    global d
#    global dx
#    global dy
#    global dz
#    
#    dxString = "diffx:  " + "%.3f" % (dx - float(dxEntry.get()))
#    testDiffx.configure(text = dxString)
#    
#    dyString = "diffy:  " + "%.3f" % (dy - float(dyEntry.get()))
#    testDiffy.configure(text = dyString)
#    
#    dzString = "diffz:  " + "%.3f" % (dz - float(dzEntry.get()))
#    testDiffz.configure(text = dzString)
#    
#    dString = "diff:  " + "%.3f" % (d - float(dEntry.get()))
#    testDiff.configure(text = dString)
    
    
    
	
    
    
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
dxLabel.grid(row=0, column=1)

dyLabel = Label(distancesLabelFrame, text = "dy:")
dyLabel.grid(row=1, column=1)

dzLabel = Label(distancesLabelFrame, text = "dz:")
dzLabel.grid(row=2, column=1)

dLabel = Label(distancesLabelFrame, text = "d:")
dLabel.grid(row=3, column=1)

recordLeftButton = Button(distancesLabelFrame, text = "Record Left Data", command = recordLeft)
recordLeftButton.grid(row=4, column=0)

recordRightButton = Button(distancesLabelFrame, text = "Record Right Data", command = recordRight)
recordRightButton.grid(row=4, column=2)

#Uncomment this, too to be able to check the correlation accuracy
#dxEntry = Entry(distancesLabelFrame, text = "dx:")
#dxEntry.grid(row=0, column=1)
#
#dyEntry = Entry(distancesLabelFrame, text = "dy:")
#dyEntry.grid(row=1, column=1)
#
#dzEntry = Entry(distancesLabelFrame, text = "dz:")
#dzEntry.grid(row=2, column=1)
#
#dEntry = Entry(distancesLabelFrame, text = "d:")
#dEntry.grid(row=3, column=1)

#testButton = Button(distancesLabelFrame, text = "Check Accuracy", command = checkAccuracy)
#testButton.grid(row=4, column=1)
#
#testDiffx = Label(distancesLabelFrame, text = "DiffX")
#testDiffx.grid(row=0, column=2)
#
#testDiffy = Label(distancesLabelFrame, text = "DiffY")
#testDiffy.grid(row=1, column=2)
#
#testDiffz = Label(distancesLabelFrame, text = "DiffZ")
#testDiffz.grid(row=2, column=2)
#
#testDiff = Label(distancesLabelFrame, text = "Diff")
#testDiff.grid(row=3, column=2)

#testDiffPercent = Label(distancesLabelFrame, text = "DiffPercent")
#testDiffPercent.grid(row=4, column=2)


bottomBar = Label(master)
bottomBar.grid(row=2)



#Mouseclick event, calls relevant functions on user click
leftLabel.bind("<Button 1>",leftCameraClick)
rightLabel.bind("<Button 1>",rightCameraClick)

print "about to update"


master.after(1000, update)
mainloop()

