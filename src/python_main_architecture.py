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
from time import sleep
from picamera import PiCamera
from picamera.array import PiRGBArray
camera = PiCamera()
camera.resolution = (480, 320)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(480, 320))

def main()

#setup part,done once (not in order)

map1, map2 = images.undistort_img()
#pwm.pwm_setup()
uls.setup()

uls_seuil=60
uls=0
stop=0
traffic=0


forframe in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	
	img = frame.array

	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	#frame=cv2.remap(frame,map1,map2,interpolation=cv2.INTER_LINEAR)

	white, red, yellow, green = images.get_color_masks(img,window=20)

	ret_stop= images.detect_stop(red)
	value_color= images.detect_lights(red,yellow,green) 
	cx = images.detect_line(white)
	uls_distance = uls.get_distance()

	if (uls_distance < seuil):
		pwm.pwm_motor(400)
	elif (ret_stop):
		pwm.pwm_motor(400)
		sleep(2)
	elif (value_color<2):
		pwm.pwm_motor(400)
		
	else:
		pwm.pwm_motor(420)
		if (cx!=0):
			place = cx/64
			
			valeur= 280+(15*place)
			pwm.pwm_turn(valeur)

pwm.motor(400)
pwm.cleanup()















#declare main() as the main function
if__name__== "__main__" 
	main()
