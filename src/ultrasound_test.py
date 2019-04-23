from time import sleep
from time import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(24,GPIO.IN)
GPIO.output(23,False)
sleep(0.5)

While True:
	GPIO.output(23,True)
	sleep(0.00001)
	GPIO.output(23,False)
	start=time()
	while GPIO.input(GPIO_ECHO)==0:
		start = time()

	while GPIO.input(GPIO_ECHO)==1:
		stop = time()



	# Distance pulse travelled in that time is time
	# multiplied by the speed of sound (cm/s)
	distance = ((stop-start) * 33100)/2



	print("Distance : {0:5.1f}".format(distance))

# Reset GPIO settings
GPIO.cleanup()