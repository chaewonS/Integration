import RPi.GPIO as GPIO
import time

from TTS import dest_reader
from TTS import txt_reader

# GPIO.setmode(GPIO.BCM)

Start_Pin = 21
Desti1_Pin = 20     # library -> 1
Desti2_Pin = 16     # music   -> 2
Desti3_Pin = 1     # music   -> 2
Desti4_Pin = 7     # music   -> 2

GPIO.setup(Start_Pin, GPIO.IN)
GPIO.setup(Desti1_Pin, GPIO.IN)
GPIO.setup(Desti2_Pin, GPIO.IN)
GPIO.setup(Desti3_Pin, GPIO.IN)
GPIO.setup(Desti4_Pin, GPIO.IN)

def detect_start():
    start_time = time.time()

    while True:
        if time.time() - start_time > 60:   # 1분 이상 버튼을 안누르면
            return 0
        if GPIO.input(Start_Pin) == 0:
            print("시작 버튼 눌림")
            return 1
        else:
            print("--시작 버튼 감지 파트--")
            time.sleep(0.2)

def set_destination():
    while True:
        if GPIO.input(Desti1_Pin) == 0:
            print("도서관 버튼 눌림")
            dest_reader(1)
            txt_reader("ment3")     # 없어도 됨
            return 1   
        elif GPIO.input(Desti2_Pin) == 0:
            print("음악실 버튼 눌림")
            dest_reader(2)
            txt_reader("ment3")     # 없어도 됨
            return 2
        else:
            print("--목적지 선택 파트--")
            time.sleep(0.2)

