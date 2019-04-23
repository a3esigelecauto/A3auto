#this is an abstract architectur of the code
#it is a busy-loop with possibly interupts added latter
#use of tabs instead of 4 spaces, cause if done in a test editor this is going
#to lead to execution errors on the raspberry
#the imports of our other python files
import pwm
import images
import ultrasound as uls
import cv2
import numpy
 

def main()

#setup part,done once (not in order)

map1, map2 = images.undistort_img()
pwm.pwm_setup()
uls.setup()
cap = cv2.videoCapture(0)

uls_seuil=40
stop_seuil=40
feux_seuil=40


while True :

	ret, frame = cap.read()
	frame = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	frame=cv2.remap(frame,map1,map2,interpolation=cv2.INTER_LINEAR)

	white, red, yellow, green = images.get_color_masks(frame,window=20)
#the following may be done in concurrency


	ret,stop_distance = images.detect_stop_distance(red)
	color,feux_distance = images.detect_lights(red,yellow,green) #feux_distance not implemented yet
	#returned = images.detect_white_line(white)
	uls_distance = uls.get_distance()

	if (uls_distance < seuil):
		pwm.motor(400)
	elif (stop_distance < stop_seuil):
		pwm.motor(400)
	elif ((color<2) and (feux_distance<feux_seuil)):
		pwm.motor(400)
	else:
		pwm.motor(420)
		#pwm.turn(something)

pwm.motor(400)
pwm.cleanup()















#declare main() as the main function
if__name__== "__main__" 
	main()
