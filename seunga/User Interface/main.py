import RPi.GPIO as GPIO
import time
from TTS import txt_reader

from find_user import *
from TTS import *
from button import *
from ultrasound import *
from vibration import *
from path import *

PIR1 = 23
PIR2 = 24
GPIO.setup(PIR1, GPIO.IN)
GPIO.setup(PIR2, GPIO.IN)

MAG_SCL = 3
MAG_SDA = 2

START_BUTTON = 21
BUTTON1 = 20
BUTTON2 = 16
BUTTON3 = 1
BUTTON4 = 7
GPIO.setup(START_BUTTON, GPIO.IN)
GPIO.setup(BUTTON1, GPIO.IN)
GPIO.setup(BUTTON2, GPIO.IN)
GPIO.setup(BUTTON3, GPIO.IN)
GPIO.setup(BUTTON4, GPIO.IN)

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

LEFT = 16
RIGHT = 20
GPIO.setup(LEFT, GPIO.OUT)
GPIO.setup(RIGHT, GPIO.OUT)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


queue = []      # 진행 경로가 들어있는 큐

def intro():
    # 사용 - 1 / 대기 - 0
    USING = 0

    while True:
        if USING == 1:
            print("1")
            # 스레딩 처리하기. 음성 듣는 중에도 버튼 누르면 동작하도록
            
            DEST = set_destination()        # 목적지 정보 획득
            perform(DEST)                   # 현재 위치 파악, 경로 탐색, 경로 안내

        elif USING == 0:
            print("0")
            USING = detecting_people()


def perform(DEST):
    route = finding_route(DEST)             # 목적지까지의 경로 탐색
    while True:
        # 현재 위치 = location()
        # 현재 위치와 예상 경로가 일치하는지 확인해야함.
        # if 경로와 내 위치가 일치하지 않을 경우:     현재 위치 not in route
        #       route = finding_route(DEST) -> 다시 탐색    
        # while 현재 위치에서 다음 route까지 피드백 제공:
        #   피드백 줌(진동, 음성 등등)
        # 만약 코너이면, 

        while True:
            # 경로 안내 하면서, 장애물 감지도 해야함 -> threading 
            if ultrasound_sensing() == 0:       # 초음파 1m 이내에 장애물 감지 되면
                obstacle()

            while queue:
                node = queue.pop(1)


if __name__ == "__main__":
    # proc1 = Thread(target=ultrasound_sensing, args=())
    # proc2 = Thread(target=obstacle, args=())
    # proc3 = Thread(target=txt_reader, args=())
    # proc1.start()
    # proc2.start()
    # proc3.start()
    intro()        
    GPIO.cleanup()
