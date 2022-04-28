import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

pin = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.OUT)

GPIO.output(pin, True)

pwm = GPIO.PWM(pin, 262)
pwm.start(50.0)
time.sleep(1)
pwm.stop()

GPIO.output(pin, False)
GPIO.cleanup()