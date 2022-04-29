import RPi.GPIO as GPIO
import time

from find_user import *
from TTS import *
from button import *
from ultrasound import *
from vibration import *
from path import *
from location import *
from find_route_coor import *
from navigate import *

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

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
            print("1")
            # 스레딩 처리하기. 음성 듣는 중에도 버튼 누르면 동작하도록
            
            DEST = set_destination()        # 목적지 정보 획득
            # 장애물 감지 처리 해줘야함
            perform(DEST)                   # 현재 위치 파악, 경로 탐색, 경로 안내

        elif USING == 0:
            print("0")
            USING = detecting_people()


def perform(DEST):   
    global done
    done = navigate(DEST)         # 경로 탐색 + 안내, 목적지 도착할 때까지 못빠져나옴.
    if done:
        print("목적지에 도착했습니다.")

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
    gth = Thread(target = geomagnetic_thread)
    gth.daemon = True

    lth = Thread(target = location_thread)
    lth.daemon =True

    try :
        gth.start()
        lth.start()
    except KeyError:
        #os.system('sudo python make_json.py')
        None

    intro()        