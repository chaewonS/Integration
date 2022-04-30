# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

LEFT = 12
RIGHT = 8

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

def vib_left():					# time은 회전 각도에 따라
	GPIO.output(LEFT, True)
	# time.sleep(1)
	# GPIO.output(LEFT, False)

def vib_right():
	GPIO.output(RIGHT, True)

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

# vib_left()
