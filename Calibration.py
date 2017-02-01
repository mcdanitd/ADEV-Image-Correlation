import numpy as np
import cv2
import glob
import time

class Calibration:
    
    def __init__(self):
        pass
    
    def recursivePowerSet(self, points, iters, last, depth, maxdepth):
        if depth>maxdepth:
            return ones
        for i in range(last+1,iters+1 - maxdepth):
            ret = points[i]
            return ret + (self.recursivePowerSet(points, iters, i, depth + 1, maxdepth))
            
            
            
    def mayn(self):
        print 'Start'
        
        cam = cv2.VideoCapture(1)
        
        
        iters=100
        error_allowed = .10
        col_min = 580
        row_min = 400
        
        mean_error=1
        x,y,w,h = (0,0,0,0)
        
        
        while(mean_error>error_allowed or w-x<col_min or h-y<row_min):
            
            objpoints, imgpoints, gray = self.collectImages(cam,iters)
            
#            imgpointsubsets = self.p([imgpoints])
#            objpointsubsets = self.p([objpoints])
##            
#            for depth in range(10, iters+1):
#                imgpointsubsets = self.recursivePowerSet(imgpoints, iters, -1, 0, depth)
#                objpointsubsets = self.recursivePowerSet(objpoints, iters, -1, 0, depth)
#            for setNum in xrange(len(imgpointsubsets)):
#                ret_val, img = cam.read()
#                ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpointsubsets[setNum], imgpointsubsets[setNum], gray.shape[::-1],None,None)       
#                h, w = img.shape[:2]
#                newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))     
#                x,y,w,h = roi  
##                print h-y
##                print w-x
#                            
#                tot_error = 0
#                for i in xrange(len(objpointsubsets[setNum])):
#                    imgpoints2, _ = cv2.projectPoints(objpointsubsets[setNum][i], rvecs[i], tvecs[i], mtx, dist)
#                    error = cv2.norm(objpointsubsets[setNum][i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
#                    tot_error += error
#                ## want 0
#                mean_error=tot_error/len(objpointsubsets[setNum])
##                print "total error: ", mean_error
#                if(mean_error<error_allowed and w-x>col_min and h-y>row_min):
#                    np.savez('calibFile2.npz', mtx, dist, newcameramtx, roi)
#                    error_allowed = mean_error
#                    col_min = w-x
#                    row_min = h-y
#                    print "total error: ", mean_error
#                    print "cols: ", col_min
#                    print "rows: ", row_min
#                    print "-------------"
#            
#            
            
            
            for one in range(0,iters):
                for two in range(one,iters):
                    for three in range(two, iters):
                        for four in range(three,iters):
                            for five in range(four,iters):
                                for six in range(five,iters):
                                    for seven in range(six,iters):
                                        for eight in range(seven,iters):
                                            for nine in range(eight,iters):
                                                for ten in range(nine,iters):
                                                    objpointsSet = [objpoints[one], objpoints[two], objpoints[three], objpoints[four], objpoints[five], objpoints[six], objpoints[seven], objpoints[eight], objpoints[nine], objpoints[ten]]
                                                    imgpointsSet = [imgpoints[one], imgpoints[two], imgpoints[three], imgpoints[four], imgpoints[five], imgpoints[six], imgpoints[seven], imgpoints[eight], imgpoints[nine], imgpoints[ten]]
                                                    ret_val, img = cam.read()                                                    
                                                    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpointsSet, imgpointsSet, gray.shape[::-1],None,None)       
                                                    h, w = img.shape[:2]
                                                    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))     
                                                    x,y,w,h = roi  
#                                                    print h-y
#                                                    print w-x
                                                                
                                                    tot_error = 0
                                                    for i in xrange(len(objpointsSet)):
                                                        imgpoints2, _ = cv2.projectPoints(objpointsSet[i], rvecs[i], tvecs[i], mtx, dist)
                                                        error = cv2.norm(imgpointsSet[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2)
                                                        tot_error += error
                                                    ## want 0
                                                    mean_error=tot_error/len(objpointsSet)
#                                                    print "total error: ", mean_error
                                                    if(mean_error<error_allowed and w-x>col_min and h-y>row_min):
                                                        np.savez('calibFile2.npz', mtx, dist, newcameramtx, roi)
                                                        error_allowed = mean_error
                                                        col_min = w-x
                                                        row_min = h-y
                                                        print "total error: ", mean_error
                                                        print "cols: ", col_min
                                                        print "rows: ", row_min
                                                        print "-------------"
                                                    
           
#        np.savez('calibFile.npz', mtx, dist, newcameramtx, roi)
        
        while True:
            
            ret_val, img = cam.read()
        
            dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
            cv2.imshow('dist', img)
            cv2.imshow('undist1u', dst)
            if(h-y>0 and w-x>0):
                dst = dst[y:y+h, x:x+w]
            
                cv2.imshow('undist1', dst)
            
        #    mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
        #    dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
        #    
        #    cv2.imshow('undist2u', dst)
        #    if(h-y>0 and w-x>0):
        #        dst = dst[y:y+h, x:x+w]    
        #    
        #        cv2.imshow('undist2', dst)
            
            if cv2.waitKey(1) == 27:
                break #esc to quit
        
        
        
        SystemExit
    
    def collectImages(self, cam, iters):    
    
        # termination criteria
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((6*7,3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
        
        # Arrays to store object points and image points from all the images.
        objpoints = [] # 3d point in real world space
        imgpoints = [] # 2d points in image plane.
        
        #images = glob.glob('*.jpg')
        
        rounds = 0
        
        delayValue = 20
        delay = delayValue
        #for fname in images:
        while rounds<iters:
            delay+=1
            if(delay<delayValue):
                time.sleep(.01)
            
            #img = cv2.imread(fname)
            ret_val, img = cam.read()
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            #cv2.imshow('my webcam', gray)
            
            # Find the chess board corners
            ret, corners = cv2.findChessboardCorners(gray, (7,6),None)
        
            # If found, add object points, image points (after refining them)
            if ret == True and delay>delayValue:
                delay=0
                rounds+=1
                print 'Found!'
                print rounds
                objpoints.append(objp)
        
                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)
            
                # Draw and display the corners
                img = cv2.drawChessboardCorners(img, (7,6), corners2,ret)
                
        #    if rounds>200:
        #        delay = 20
        #        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)       
        #  
        #        h, w = img.shape[:2]
        #        newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
        #        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        #
        #        # crop the image
        ##        x,y,w,h = roi
        ##        print '6'
        ##        dst = dst[y:y+h, x:x+w]   
        ##        print '7'
        #        cv2.imshow('undist', dst)
                
                
                
            cv2.imshow('gray',gray)
            cv2.imshow('img',img)
                
        
            if cv2.waitKey(1) == 27:
                break #esc to quit
                
        return (objpoints, imgpoints, gray)        
        cv2.destroyAllWindows()
    
    