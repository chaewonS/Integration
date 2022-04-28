from threading import Thread
import RPi.GPIO as GPIO
import time

from TTS import *
from button import *

GPIO.setmode(GPIO.BCM)

# range pin
# 1m - False / 3m - True

OUT1 = 25
RANGE1 = 8
GPIO.setup(OUT1, GPIO.IN)
GPIO.setup(RANGE1, GPIO.OUT)
GPIO.output(RANGE1, False)

OUT2 = 22
RANGE2 = 27         # 확인 필요
GPIO.setup(OUT2, GPIO.IN)
GPIO.setup(RANGE2, GPIO.OUT)
GPIO.output(RANGE2, False)


def ultrasound_sensing():
    while True:
        if GPIO.input(OUT1) == 0 or GPIO.input(OUT2) == 0:
            return 0

# 출력
# 감지 - 0 / 미감지 - 1