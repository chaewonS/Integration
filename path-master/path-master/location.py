# -*- coding: utf-8 -*-

import io
import blescan
import sys
import bluetooth._bluetooth as bluez
import json
import threading
import time
from collections import Counter
import loc

with io.open('./pair.json') as f:
    info = json.load(f)

#====================================Classes============================================
class Beacon():
    def __init__(self, mac, rssi):
        self.MAC = mac

    # self.X = 'MAC 주소 활용해서 만들어진 test.json파일에서 가져온 X'
    # 비콘 x, y 좌표 출력 부분 추가

        self.X = int(info[mac]["location"].split(',')[0])
        self.Y = int(info[mac]["location"].split(',')[1])
        self.RSSI = int(rssi) #거리 반비례 변수, *음수도 정수 변환 가능 *
        # self.G = int(info[mac]["group"])

    def getX(self):
        return self.X

    def getY(self):
        return self.Y

    def getXY(self):
        return self.X, self.Y

    def getRSSI(self):
        return self.RSSI

    def getMAC(self):
        return self.MAC

    # def getG(self):
    #     return self.G
#========================================= End Of Classes ============================================
beacon_list =[]
pairs = []

dev_id = 0 #scan
#========================================== Definition Of Functions ==================================
#FB301BC 초기 설정 TxPower = 41
def calculateDistance(rssi) :
    txPower = -16
    if (rssi == 0) :
        return -1.0 #if we cannot determine distance return -1.
    ratio = rssi*1.0/txPower #
    if (ratio < 1.0) :
        return ratio**10

    else:
        accuracy =  (0.89976)*(ratio**7.7095) + 0.111
        return accuracy
# #https://github.com/location-competition/indoor-location-competition-20

def simpleDistance(rssi):
    TxPower = 41
    return 10 ** ((TxPower - rssi )/(10*4)) # 4 = n : 실내공간

def find_pair(mac):
    my_group = int(info[mac]["group"])
    return my_group


def get_loc():
    # print("여기도 대충 뭐 현재 위치 가져오는 함수")
    # # 현재 위치를 스레싱 처리해서 계속 가져오게 하는게 좋을 듯??
    # return 12,28
    return loc.now_loc

def location_thread():
    best = []   # 현재 위치(그룹)을 모아 놓은 리스트

    try:
        sock = bluez.hci_open_dev(dev_id)
        print("ble thread started")

    except:
        print ("error accessing bluetooth device...")
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

    while True:
        maclist = []
        returnedList = blescan.parse_events(sock, 10)

        for beacon in returnedList:
            if beacon[:5] == "00:19":
                beacon = beacon.split(",")
                beacon_list.append([beacon[0],beacon[5]])   # MAC, RSSI

            # print(beacon_list)

            pair = []       # 비콘의 맥, 그룹, rssi
            if len(beacon_list) == 13:
                for g in beacon_list:
                    pair.append([g[0],find_pair(g[0]),g[1]])

                result = []     # 그룹, rssi
                i = 0
                for j in pair:
                    for k in pair[i+1:]:
                        if j[0] != k[0] and j[1] == k[1]:
                            j[2] = int(j[2])
                            aver = int((k[1]+j[1])//2)
                            result.append([j[2],aver])
                    i += 1
                    
                if len(result) > 0:         # 비콘 그룹을 찾았을 때
                    group = max(result)
                    print("group: ",group)
                    best.append(group[1])

                beacon_list = []

                if len(best) == 3:          # 현위치 3개가 모였을 때, 최빈 값 찾는 코드
                    best_count = Counter(best).most_common(1)
                    print("----------------------------")
                    print("my location",best_count[0][0])
                    loc.now_loc = best_count[0][0]
                    print("----------------------------")
                    best = []
