from threading import Thread
import RPi.GPIO as GPIO
import time

from TTS import *
from button import *

PIR1 = 23
PIR2 = 24
GPIO.setup(PIR1, GPIO.IN)
GPIO.setup(PIR2, GPIO.IN)

def detecting_people():
    while True:
        # 사람이 2초 이상 감지되면 등으로 조건 추가
        # 감도가 너무 높음
        if GPIO.input(PIR1) or GPIO.input(PIR2):
            txt_reader("ment1")         # 장치가 여기있음을 홍보
            if detect_start() == 1:
                txt_reader("ment2")     # 사용 방법 안내
                return 1
            else:
                return 0
        else:
            print("No motion")
            return 0


# pir로 사람 감지 후, 2번 방송. 
# if 방송 중에 시작 누르면 방송 종료 후 시작