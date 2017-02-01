
cameraMaxHorzAngle = 120
cameraMaxVertAngle = 120
depthMaxHorzAngle = 120
depthMaxVertAngle = 120
separation = 1




for(pixel in depthArray):
	A = ((xvalue/depthColumns)*depthMaxHorzAngle)-90
	#if distance values aren't along the hypotenuse add next line
	#x = pixel*cos()
	#otherwise
	x=pixel

	# for left webcam
	if(A>0):
		C=A+90
	else:
		C = 90-A
	w = sqrt(x^2+separation^2 - 2*x*separation*cos(C)) # add some correction for C>90
	D = arcsin(x*sin(C)/w)
	B = 90 - D
	lWebcamXValue = B+90*webcamColumns/depthMaxHorzAngle
	#this is wrong, but close, need to throw in a factor for max vertical angle
	lWebcamYValue = (yvalue/depthRows)*webcamRows




