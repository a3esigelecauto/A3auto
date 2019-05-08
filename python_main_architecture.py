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
camera = PiCamera()#set up the picamera for 30 fps and a 320*240 resolution
camera.resolution = (320,240)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(320,240))

def main():

	#setup part,done once (not in order)

	#map1, map2 = images.undistort_img()
	ser = serial.Serial('/dev/ttyACM0', 115200)#the serial communication through usb to the arduino
	uls_seuil=60
	
	
	uls=0#flag to check if the car is in the obstace-detected mode
	stop=0#flag to check if the car is in the stop-detected mode
	traffic=0#flag to check if the car is in the traffic-detected mode
	
	stop_flag=0#gets to one if a stop is detected
	stop_flag_2=0#once a stop has been detected this will increment until a certain number before the car will start detecting stop again
	stop_done=0
	stop_done_check=0
	
	
	traffic_flag=0
	traffic_flag_2=0
	traffic_done=0
	
	motor=0
	turn=0
	time.sleep(1)
	
	virage_last=0#value of turn currently in use in the servo(so we don't sned a new command if the value remains unchanged
	cx_last=0#used to check if the nex cx is not to different from the last so a sudden white spot like a wall won't influenc the car
	
	cx_start=0#the first value of cx
	
	for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
		
		if stop_flag<0:#preventt his value from being negative
			stop_flag=0
			
		if stop_flag_2!=0:#if a stop has been detected it won't track from a new stop for a certain time
			stop_flag_2+=1
			if stop_flag_2==7:
				stop_flag=0
				stop_flag_2=0
				
		if traffic_flag<0:#prevent this value from being negative
			traffic_flag=0
			
		if traffic_flag_2!=0:#if a traffic ligth has been detected 
			traffic_flag_2+=1
			if traffic_flag_2==7:
				traffic_flag=0
				traffic_flag_2=0
			
		img = frame.array#get the new image

		img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)#transform the image into the hsv format
		
		white, red,green = images.get_color_masks(img,level=40)#return the white, red and green masks
		
		ret_stop,distance= images.detect_stop(red)#return if it has detected a stop and if yes it's distance
		
		img2=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
		value_color= 0#images.detect_lights(img2,red,green)
		
		
		cx = images.detect_line(white)#return the centroid of theline if it detected one
		if cx_start==0:#if this is the first frame this condition put the recored one to be same as the newly detected one
			cx_last=cx
			cx_start=1
		
		serial_value = ser.read()#get the 1 or 0 depending if an obstacle was detected
		ser.reset_input_buffer()#delete the \r and \n from the input buffer
		uls_distance = serial_value.decode()#get the string from the byte 
		if uls==0:#if not in a stat were an obstacle was detected before, check if one just got detected
			if (uls_distance =="1"):#if yes put the state to obstacle and goes to the next iteration
					ser.write(b'300')
					print("obstacle")
					uls=1
					rawCapture.truncate(0)
					continue
		else:#if in a state of an obstacle detected before check if there is none anymore and free the car if it is the case
			if (uls_distance =="0"):
					print("fin obstacle")
					uls=0
					rawCapture.truncate(0)
					continue
			else:
				rawCapture.truncate(0)
				continue
		
					
		if stop_done==0:#if not in the stop-detected state		
			if ((ret_stop==1) and (distance<=100)):#if one has been detected close enough, stops the car, wait 2 seconds then trigger the stop-detected state
			#so it won't try to check for another one before 35 frames
				stop_flag+=1
				stop_flag_2=1
				print("detect stop")
				if (stop_flag>=3):#this is used to check if a stop has been detected in multpile frame to prevent false positive
					ser.write(b'300')
					print("stop")
					stop_flag=0
					stop_done=1
					stop_done_check=35
					time.sleep(2)
					rawCapture.truncate(0)
					continue
		elif stop_done==1:#if in the stop_detected state and the counter ran to zero, let the car be able to check for a stop again
			stop_done_check-=1
			if (stop_done_check<=0):
				stop_done_check=0
				stop_done=0
			value_color=0
			
			
		if (traffic_done==0):
			#if a traffic has been detected, stops the car until it doesn't detect one		
			if (value_color==2):
				print("traffic_spoted")
				traffic_flag+=1
				traffic_flag_2+=1
				if (traffic_flag>=5):#this is used to check that the traffic has been detected on multiplt frame before stopping
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
		if (cx!=0):#in the case nothing but a line was detected compute the value to be sent to th eservo of the car beteween 60 and 114
			if abs(cx-cx_last)<=50:#check that the new centroid is not too far from the previous one so the car isn't oinfluenced by false positive
				slice=int(cx/32)
				virage=60+6*slice
				print(slice)
				cx_last=cx
				if (virage!=virage_last):#only send the value if the virage o do is different from the actual one
					ser.write(str(virage).encode("latin1"))
					#print(str(virage).encode("latin1"))
					virage_last=virage
				else:
					ser.write(b'1585')
			
		else:#this happens if nothing at all was detected
			#ser.write(b'300')
			print("pas de ligne")
			
		
		rawCapture.truncate(0)#frre the camera receiver for the next frame
	ser.write(b'240')















#declare main() as the main function
if __name__== "__main__": 
	main()
