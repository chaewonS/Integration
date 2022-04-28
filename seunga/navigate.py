from location import *
from find_route_coor import *
from geomagnetic import *
from vibration import *

me = -1             # 내가 보고 있는 방향 각도
want = -1           # 가야하는 방향 각도
change = -1         # 현재 보고 있는 x, y 축 진행 방향 정보 / x=0, y=1

route_len = -1
now_index = 0

pre_loc = (-1, -1)
now_loc = (-1, -1)
next_loc = (-1, -1)

def navigate(DEST):
    # 전체 초기화 과정
    now_loc = get_loc()
    route = Graph.a_star_algorithm(now_loc, DEST)
    route_len = len(route)
    want = xy_direction(route[0],route[1])        # 첫 진행 방향 초기화
    me = get_angle()

    while now_loc != DEST:

        pre_loc = now_loc
        now_loc = get_loc() # 이렇게 할 게 아니라 스레딩 처리해서 위치를 계속 가져와야 함
        
        # 값이 튄 경우 / 현재 감지한 x,y와 이전 위치의 x,y 값이 4 이상 차이 나면
        if abs(now_loc[0]-pre_loc[0]) >= 4 or abs(now_loc[1]-pre_loc[1]) >= 4:
            now_loc = route[route.index(pre_loc)+1]     # 루트 상의 이전(직전에 방문한) 노드의 다음 노드를 넣어줌
            
        now_index = route.index(now_loc)
        next_loc = route[now_index+1]


        if now_loc not in route:        # 경로에서 이탈했으면
            now_index = 0
            navigate(DEST)
            # route = Graph.a_star_algorithm(now_loc, DEST)


        want = xy_direction(now_loc, next_loc)
        me = get_angle()    # 각도도 계속 가져오면 좋겠음!

        if (want-10) >= me and me >= (want+10):    # 내가 보고 있는 방향이 진행 방향이 아니라면,
            turn_direction = turn(want, me)
            if turn_direction == 'right':
                while (want-10) >= me and me >= (want+10):  # 목표 방향 +-10 이내가 될 때 까지
                    vib_right()     # 진동을 발생
            elif turn_direction == 'left':
                while (want-10) >= me and me >= (want+10):  # 목표 방향 +-10 이내가 될 때 까지
                    vib_left()      # 진동을 발생

    return 1

def xy_direction(now, next):
    x1 = now[0];    y1 = now[1]
    x2 = next[0];    y2 = next[1]
    x = x1 - x2;         y = y1 - y2

    if x > 0:           # x 좌표가 감소했으면
        return 0        # 북측 0도
    elif x < 0:
        return 2        # 남측 180도
    elif y > 0:         
        return 3        # 서측 270도
    elif y < 0:         
        return 1        # 동측 90도


def turn(want, me):         # 방향 맞출 때 왼쪽으로 도는게 빠른지, 오른쪽으로 도는게 빠른지
    left = 360 - want + me
    right = want - me

    if right >= left:
        return 'left'       # 방향을 알리는 str을 반환하는데, 각도로 반환해서 시간 계산 진동 발생도 가능할 듯
    else:
        return 'right'
