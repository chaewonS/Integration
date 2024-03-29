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
    my_group = info[mac]["group"]
    return my_group


def get_loc():
    # print("여기도 대충 뭐 현재 위치 가져오는 함수")
    return loc.now_loc

def location_thread():
    best = []   # 현재 위치(그룹)을 모아 놓은 리스트
    final_best = []

    try:
        sock = bluez.hci_open_dev(dev_id)
        print("ble thread started")

    except:
        print ("error accessing bluetooth device...")
        sys.exit(1)

    blescan.hci_le_set_scan_parameters(sock)
    blescan.hci_enable_le_scan(sock)

    beacon_list = []
    while True:
        returnedList = blescan.parse_events(sock, 10)

        for beacon in returnedList:
            if beacon[:5] == "00:19":           # 우리의 fc 친구들만 모아
                beacon = beacon.split(",")
                beacon_list.append([beacon[0],beacon[5]])   # MAC, RSSI만 리스트에 넣기

            # print(beacon_list)

            pair = []       # 비콘의 맥, 그룹, rssi
            if len(beacon_list) == 10:          # 그룹 매칭 단위
                for g in beacon_list:
                    # g[0]: MAC, g[1]: RSSI
                    pair.append([g[0],tuple(find_pair(g[0])),g[1]])    # MAC과 그룹 번호 저장

                result = []     # rssi, 그룹 / 커플만 있음.
                i = 0

                #print("pair:",pair)

                for j in pair:
                    for k in pair[i+1:]:    # pair 전체를 돌면서 쌍 매칭
                        # j[0]: MAC, j[1]: 그룹, j[2]:rssi
                        if j[0] != k[0] and j[1] == k[1]:   # 맥은 다르고 rssi는 같으면
                            j[2] = int(j[2])
                            aver = int((int(k[2])+int(j[2]))//2)
                            result.append([aver,j[1]])
                    i += 1

                if len(result) > 0:         # 비콘 그룹이 있을 때
                    # print("result:",result)
                    group = max(result)     # 
                    # print("group: ",group)
                    best.append(group[1])

                beacon_list = []
		#print(beacon_list)

                if len(best) == 13:          # 현위치 3개가 모였을 때, 최빈 값 찾는 코드
                    # print("----------------------------")
                    best_count = Counter(best).most_common(1)
                    #print(best_count)
                    #print(best_count[0])
                    #print(best_count[0][0])
                    final_best.append(best_count[0][0])
                    #아래 출력하면 됨
                    # print('my_location: ', best_count[0][0])
                    # print(best, 'my_location:', best_count[0][0])
                    #아래 출력하면 됨
                   # loc.now_loc = best_count[0][0]
                    # print("----------------------------")
                    best = []

		if len(final_best) == 8:
                   final_best_count = Counter(final_best).most_common(1)
                   print(final_best_count[0][0])
                  # temp = (12, 29)
                  # for (i,j) in final_best_count:
                  #     temp = i
                  #     for (m,n) in final_best_count:
                  #       if m != temp:
                  #         print(m)
                  #       else:
                  #         print("같은 위치입니다.")
                  # for index, (i,j) in enumerate(final_best_count):
                  #     temp = i
                  #     if temp != i:
                  #      print(index, i)
                  #     else:
                  #      print("계속해서 같은 위치입니다.")
                  # for (i,j) in final_best_count:
                  #    if i != i+1:
                  #      print(i)
                  #    else:
                  #      print("계속해서 같은 위치입니다.")
                  #     pre = i
                  #     print(i)
                  #     if pre != i+1:
                  #     	 print(i+1)
                  #     else:
                  #       print("계속해서 같은 위치입니다.")
                   #pre = final_best_count[0][0]
                   #for i in final_best_count:
                   #     print(final_best_count[0][0])

                #   print(final_best_count[0][0])
#                   for i in final_best_count:
#                       print(final_best_count[0][0]
#                       if (final_best_count[0][0] != final_best_count[i][0]):
#                        print(final_bect_count[i][0])
 #                  pre = final_best_count
  #                 for now in final_best_count:
   #                    if pre != now:
    #                     print(final_best_count[0][0])
                   #print('my final location:', final_best_count[0][0])
                   loc.now_loc = final_best_count[0][0]
                   final_best = []

if __name__ == "__main__":
	get_loc()
	location_thread()

