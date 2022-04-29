import RPi.GPIO as GPIO
import time

LEFT = 16
RIGHT = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(LEFT, GPIO.OUT)
GPIO.setup(RIGHT, GPIO.OUT)

def once():
	GPIO.output(LEFT, True)
	time.sleep(3)
	GPIO.output(LEFT, False)

def obstacle():
	GPIO.output(LEFT, True)
	time.sleep(0.2)
	GPIO.output(LEFT, False)

def vib_left(time):					# time은 회전 각도에 따라
	GPIO.output(LEFT, True)
	time.sleep(time)
	GPIO.output(LEFT, False)

def vib_right(time):
	GPIO.output(RIGHT, True)
	time.sleep(time)
	GPIO.output(RIGHT, False)

def vib_stop():
    GPIO.output(LEFT, False)
    GPIO.output(RIGHT, False)

# PWM
# myPwm = GPIO.PWM(LEFT, 1000) # LEFT, frequency
# myPwm.start(50)

# Frequency  변경 (Hz)
# myPwm.ChangeFrequency(1500)

# for i in range(100):
# 	myPwm.ChangeDutyCycle(i)	#0~100%
# 	time.sleep(0.02)
	
# myPwm.stop()

GPIO.output(LEFT, True)
time.sleep(1)
GPIO.output(LEFT, False)

# GPIO.output(RIGHT, True)
# time.sleep(1)
# GPIO.output(RIGHT, False)

# GPIO.output(LEFT, True)
# GPIO.output(RIGHT, True)
# time.sleep(1)
# GPIO.output(RIGHT, False)
# GPIO.output(LEFT, False)

# PWM
myPwm = GPIO.PWM(LEFT, 1000) # LEFT, frequency
myPwm.start(0)

for i in range(100):
	myPwm.ChangeDutyCycle(i)	#0~100%
	time.sleep(0.05)
	
myPwm.stop()