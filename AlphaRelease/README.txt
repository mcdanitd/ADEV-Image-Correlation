README.txt

Everything is run from CorrelationApp.py, except for the C++ code for the depth cam, which must be started independently. The displacement output is currently centered on the PMD lens and the coordinate system is as seen in coordinateSystem.png. 

Relevant lines to change to adjust for differences in our physical setups:
Correlator.py:
	lines 25 - 29:The first four may or may not need adjusting but I'm sure line 29 will need to be changed
	line 219 - 226: Change this to change what datum is used for the displacement output. 
camFeed.py:
	lines 98-100: These are for rotating the image to suit the way that we have our cameras mounted. You may or may not need this line, if your images come out upside down with these lines in place, just comment them out.
PMDReceiver.py:
	line 47: This line is also for rotation based on our set up, and may need to be commented out. 

I think I was good and any changes to reflect changes in setup should propogate through and give good results, but let me know if there's anything going wrong.