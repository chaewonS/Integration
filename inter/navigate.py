# -*- coding: utf-8 -*-

# from location import *
from stay1 import *
from mini_coor import *
# from find_route_coor import *
from geomagnetic import *
from vibration import *
from mini_graph import adjac_lis as adj
# from graph import adjac_lis as adj

import time

graph = Graph(adjac_lis)
def navigate(DEST):
    me = -1             # 내가 보고 있는 방향 각도
    want = -1           # 가야하는 방향 각도
    change = -1         # 현재 보고 있는 x, y 축 진행 방향 정보 / x=0, y=1

    route_len = -1
    now_index = 0

    pre_loc = (-1, -1)
    now_loc = (-1, -1)
    next_loc = (-1, -1)

    # 전체 초기화 과정
    now_loc = get_loc()
    route = graph.a_star_algorithm(now_loc, DEST)
    if route == 0:
        return 1
    route_len = len(route)
    if route_len == 1:
        return 1
    print("route:",route)
    want = xy_direction(route[0],route[1])        # 첫 진행 방향 초기화
    me = get_angle()

    while now_loc != DEST:

        if now_index >= 1:
            pre_loc = now_loc

        now_loc = get_loc() 
        print("00000000now_loc00000000>",now_loc)
        # 값이 튄 경우 / 현재 감지한 x,y와 이전 위치의 x,y 값이 3 이상 차이 나면
        if pre_loc != (-1,-1):
            if abs(now_loc[0]-pre_loc[0]) >= 5 or abs(now_loc[1]-pre_loc[1]) >= 5:
                now_loc = route[route.index(pre_loc)+1]     # 루트 상의 이전(직전에 방문한) 노드의 다음 노드를 넣어줌
                print("5 distance:",now_loc)

            # 나와 내 주변의 이웃한 노드들을 저장해놓고, 값이 그 안에 있지 않으면 튄 값으로 판별
            if now_loc not in adj[pre_loc]:
                now_loc = route[route.index(pre_loc)+1]
                print("no neighbor",now_loc)

        # 인덱스 range 초과 방지 하기 위해서
        now_index = route.index(now_loc)

        # 둘의 값이 같다는 것은, 루트의 마지막 즉, 도착지
        # 도착지 처리 해야함.
        if now_index + 1 == route_len:
            next_loc = (-1,-1)
        else:
            next_loc = route[now_index+1]       
        

        # 경로에서 이탈했으면
        if now_loc not in route:        
            now_index = 0
            navigate(DEST)


        want = xy_direction(now_loc, next_loc)
        me = get_angle()

        # 내가 보고 있는 방향이 진행 방향이 아니라면,
        if (want-10) > me or me > (want+10):    
            turn_direction = turn(want, me)
            print("진동입니다.")
            if turn_direction == 'right':
                print('[direction]: right')
                vib_right()     # 진동을 발생
                while (want-10) >= me or me >= (want+10):  # 목표 방향 +-10 이내가 될 때 까지
                    me = get_angle()
                    print('right:',me,want)
                    time.sleep(0.2)
            elif turn_direction == 'left':
                me = get_angle()
                print('[direction]: left')
                vib_left()      # 진동을 발생
                while (want-10) >= me or me >= (want+10):  # 목표 방향 +-10 이내가 될 때 까지
                    print('left:',me,want)
                    time.sleep(0.2)
        vib_stop()
        
        print('route: {0}, route len: {1}'.format(route, route_len))
        print('pre: {}, now: {}, next:{}'.format(pre_loc, now_loc,next_loc))
        print('now_index: {}'.format(now_index))
        print('me: {}, want:{}'.format(me, want))
        print('----------------------------------------------')
        time.sleep(0.2)
    return 1


def xy_direction(now, next):
    x1 = now[0];    y1 = now[1]
    x2 = next[0];    y2 = next[1]
    x = x1 - x2;         y = y1 - y2

    if x > 0:           # x 좌표가 감소했으면
        return 170        # 북측 0도
    elif x < 0:
        return 298        # 남측 180도
    elif y > 0:         
        return 244        # 서측 270도
    elif y < 0:         
        return 357        # 동측 90도


def turn(want, me):         # 방향 맞출 때 왼쪽으로 도는게 빠른지, 오른쪽으로 도는게 빠른지
    left = 360 - want + me
    right = want - me

    if right >= left:
        return 'left'       # 방향을 알리는 str을 반환하는데, 각도로 반환해서 시간 계산 진동 발생도 가능할 듯
    else:
        return 'right'
