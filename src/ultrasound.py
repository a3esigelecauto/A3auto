import time
import RPi.GPIO as GPIO

def setup():
	GPIO.setmode(GPIO.BCM)

	GPIO_TRIGGER = 23
	GPIO_ECHO    = 24

	

	GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
	GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
	# Set trigger to False (Low)
	GPIO.output(GPIO_TRIGGER, False)

	# Allow module to settle
	time.sleep(0.5)

def get_distance():


# Send 10us pulse to trigger
	GPIO.output(23, True)
# Wait 10us
	time.sleep(0.00001)
	GPIO.output(23, False)
	start = time.time()

	while GPIO.input(24)==0:
		start = time.time()

	while GPIO.input(24)==1:
		stop = time.time()

# Calculate pulse length
	elapsed = stop-start
	speedSound = 33100 
# Distance pulse travelled in that time is time
# multiplied by the speed of sound (cm/s)
	distance = elapsed * speedSound

# That was the distance there and back so halve the value
	distance = distance / 2
	return distance
	
def cleanup():
	GPIO.cleanup()