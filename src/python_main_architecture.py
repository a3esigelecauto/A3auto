#this is an abstract architectur of the code
#it is a busy-loop with possibly interupts added latter
#use of tabs instead of 4 spaces, cause if done in a test editor this is going
#to lead to execution errors on the raspberry
#the imports of our other python files
import images
import cv2
import time
import serial
import struct
from picamera import PiCamera
from picamera.array import PiRGBArray
camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(320,240))

def main():

	#setup part,done once (not in order)

	#map1, map2 = images.undistort_img()
	ser = serial.Serial('/dev/ttyACM0', 115200)
	uls_seuil=60
	
	
	uls=0
	stop=0
	traffic=0
	
	stop_flag=0
	stop_flag_2=0
	stop_done=0
	stop_done_check=0
	
	
	traffic_flag=0
	traffic_flag_2=0
	traffic_done=0
	
	motor=0
	turn=0
	time.sleep(1)
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		
		if stop_flag<0:
			stop_flag=0
			
		if stop_flag_2!=0:
			stop_flag_2+=1
			if stop_flag_2==7:
				stop_flag=0
				stop_flag_2=0
				
		if traffic_flag<0:
			traffic_flag=0
			
		if traffic_flag_2!=0:
			traffic_flag_2+=1
			if traffic_flag_2==7:
				traffic_flag=0
				traffic_flag_2=0
			
		img = frame.array

		img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		
		white, red,green = images.get_color_masks(img,level=40)
		
		ret_stop,distance= images.detect_stop(red)
		
		img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		value_color= 0#images.detect_lights(img2,red,green)
		
		
		cx = images.detect_line(white)
		
		
		serial_value = ser.read()
		ser.reset_input_buffer()
		uls_distance = serial_value.decode()
		
		if uls==0:
			if (uls_distance =="1"):
					ser.write(b'300')
					print("obstacle")
					uls=1
					rawCapture.truncate(0)
					continue
		else:
			if (uls_distance =="0"):
					print("fin obstacle")
					uls=0
					rawCapture.truncate(0)
					continue
			else:
				rawCapture.truncate(0)
				continue
		
					
		if stop_done==0:		
			if (ret_stop==1):
				stop_flag+=1
				stop_flag_2=1
				print("detect stop")
				if (stop_flag>=3):
					ser.write(b'300')
					print("stop")
					stop_flag=0
					stop_done=1
					stop_done_check=15
					time.sleep(2)
					rawCapture.truncate(0)
					continue
		elif stop_done==1:
			stop_done_check-=1
			if (stop_done_check<=0):
				stop_done_check=0
				stop_done=0
			value_color=0
			
			
		if (traffic_done==0):				
			if (value_color==2):
				print("traffic_spoted")
				traffic_flag+=1
				traffic_flag_2+=1
				if (traffic_flag>=5):
					ser.write(b'300')
					traffic_done=1
					traffic_flag=0
					stop_done=2
					print("traffic")
					rawCapture.truncate(0)
					continue
		else:
			if (value_color==1):
				print("maintenant")
				traffic_done=0
				stop_done=0
				rawCapture.truncate(0)
				continue
					
		if (cx!=0):
			slice=int(cx/32)
			virage=60+6*slice
			ser.write(str(virage).encode("latin1"))
			print(virage)
			print(str(virage).encode("latin1"))
			time.sleep(0.01)
			ser.write(b'1600')
		else:
			ser.write(b'300')
			print("pas de ligne")
			
		
		rawCapture.truncate(0)
	ser.write(b'240')















#declare main() as the main function
if __name__== "__main__": 
	main()
