from subprocess import call
from time import sleep

def pwm_setup():

	call('gpio mode 1 pwm', shell=True)
	call('gpio mode 23 pwm', shell=True)
	call('gpio pwm-ms', shell=True)
	call('gpio pwmr 4000', shell=True)
	call('gpio pwmc 77', shell=True)
	call ('gpio pwm 1 400',shell=True)
	call('gpio pwm 23 320',shell=True)
	sleep(2)
	return 0

def pwm_motor(value):

	call('gpio pwm 1 '+str(value),shell=True)
	return 0
	
def pwm_turn(value):
	
	call('gpio pwm 23 '+str(value),shell=True)
	return 0