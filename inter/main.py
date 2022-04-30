# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import threading

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

from find_user import *
# from ttts import *
from button import *
from ultrasound import *
from vibration import *
from path import *
from location import *
from find_route_coor import *
from navigate import *


MAG_SCL = 3
MAG_SDA = 2

# 사용 - 1 / 대기 - 0
USING = 0
done  = 0
queue = []      # 진행 경로가 들어있는 큐

def intro():
    global USING

    while True:
        if USING == 1:
            print("USING: 1")
            # 스레딩 처리하기. 음성 듣는 중에도 버튼 누르면 동작하도록
            
            DEST = set_destination()        # 목적지 정보 획득
            print("DESTINATION:",DEST)
            # 장애물 감지 처리 해줘야함
            perform(DEST)                   # 현재 위치 파악, 경로 탐색, 경로 안내

        elif USING == 0:
            print("USING: 0")
            USING = detecting_people()


def perform(DEST):   
    global done
    global USING
    done = navigate(DEST)         # 경로 탐색 + 안내, 목적지 도착할 때까지 못빠져나옴.
    if done:
        print("목적지에 도착했습니다.")
        USING = 0
        

if __name__ == "__main__":
    print("메인 시작 합니다.")

    gth = Thread(target=geomagnetic_thread)
    lth = Thread(target=location_thread)

    gth.daemon = True
    lth.daemon =True

    gth.start()
    lth.start()

    intro()        