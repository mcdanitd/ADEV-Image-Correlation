These files are for calibrating the webcams to remove the radial distortion.
Run CalibMain.py to take ~100 images (this number is editable in line 15 of Calibration.py) 
of the black and white chessboard provided in opencv/sources/samples/data/chessboard.png.

After the images are taken, the program loops over subsets of the images to find a combination
that removes the distortion while keeping a reasonable portion of the image. The maximum allowable
error, (I couldn't quite decipher what the error measures) can be changed in line 16. 
The minimum allowable dimensions can be edited in lines 17 and 18. Looping over all of the images 
can take quite a bit of time, and may not always result in a distortion removal matrix that fits the 
desired error, height, and width criteria. I would recommend getting a good variety of captures of 
the chessboard, and letting the loop run overnight.

A .npz file will be made that will be used by camFeed.py to remove the distortion.