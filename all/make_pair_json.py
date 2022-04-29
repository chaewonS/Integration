# -*- coding: utf-8 -*-
import io
import json

Beacon = dict()

beacon1 = dict()
beacon1["location"] = "1,1"
beacon1["place"] = "교수님랩실"
beacon1["group"] = (12,22)
Beacon["00:19:01:70:81:33"] = beacon1#
beacon2 = dict()
beacon2["location"] = "1,1"
beacon2["place"] = "좌상단"
beacon2["group"] = (12,22)
Beacon["00:19:01:70:80:d9"] = beacon2#


beacon3 = dict()
beacon3["location"] = "1,1"
beacon3["place"] = "연구실"
beacon3["group"] = (12,21)
Beacon["00:19:01:70:80:de"] = beacon3 #
beacon4 = dict()
beacon4["location"] = "1,1"
beacon4["place"] = "좌상단"
beacon4["group"] = (12,21)
Beacon["00:19:01:70:86:35"] = beacon4#


beacon5 = dict()
beacon5["location"] = "1,1"
beacon5["place"] = "학회실"
beacon5["group"] = (12,18)
Beacon["00:19:01:70:81:4e"] = beacon5#
beacon6 = dict()
beacon6["location"] = "1,1"
beacon6["place"] = "좌상단"
beacon6["group"] = (12,18)
Beacon["00:19:01:70:85:0f"] = beacon6


beacon7 = dict()
beacon7["location"] = "1,1"
beacon7["place"] = "좌상단"
beacon7["group"] = (10,18)
Beacon["00:19:01:70:81:75"] = beacon7#
beacon8 = dict()
beacon8["location"] = "1,1"
beacon8["place"] = "좌상단"
beacon8["group"] = (10,18)
Beacon["00:19:01:70:84:4b"] = beacon8 #

#--------------------
beacon9 = dict()
beacon9["location"] = "1,1"
beacon9["place"] = "좌상단"
beacon9["group"] = "5"
Beacon["00:19:01:70:81:33"] = beacon9
beacon8 = dict()
beacon8["location"] = "1,1"
beacon8["place"] = "좌상단"
beacon8["group"] = "1"
Beacon["00:19:01:70:81:33"] = beacon8

with io.open('./pair.json', 'wb',
# encoding='utf-8'
)as make_file:
    json.dump(Beacon, make_file)
print("위치 좌표 파일이 현재 위치에 'pair.json'으로 갱신되었습니다.")
