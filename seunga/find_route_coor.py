from collections import deque

class Graph:
    def __init__(self, adjac_lis):
        self.adjac_lis = adjac_lis

    def get_neighbors(self, v):
        return self.adjac_lis[v]

    # 모든 노드에 대해 동일한 값을 갖는 휴리스틱 함수.
    def h(self, n):
        H = {
            (12,31) : 1,
            (12,28) : 1,
            (12,16) : 1,
            (12,24) : 1,
            (12,28) : 1,
            (12,21) : 1,
            (9,21) : 1,
            (10,19) : 1,
            (12,18) : 1,
            (12,20) : 1,
            (12,17) : 1,
            (12,16) : 1,
            (12,13) : 1,
            (12,12) : 1,
            (12,11) : 1,
        }

        return H[n]

    def a_star_algorithm(self, start, stop):

        open_lst = set([start])  # 방문한 적이 있는 노드 목록(이웃이 항상 검사되는 것은 아님)
                                 # start부터 시작됨.                                    
        closed_lst = set([])  # 방문한 노드의 목록(이웃은 항상 검사 완료됨.)

        poo = {}  # 시작부터 다른 모든 노드 까지의 현재 거리를 갖고 있음.
                  # 기본 값은 +무한대 임.
        poo[start] = 0

        par = {}  # 모든 노드의 adjac 매핑을 포함함.
        par[start] = start

        while len(open_lst) > 0:
            n = None

            # f()값이 가장 낮은 노드를 찾는다
            for v in open_lst:
                if n == None or poo[v] + self.h(v) < poo[n] + self.h(n):
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            if n == stop:   # 만약 현재 노드가 stop인 경우 처음부터 다시시작함.
                reconst_path = []  

                while par[n] != n:
                    reconst_path.append(n)
                    n = par[n]

                reconst_path.append(start)

                reconst_path.reverse()

                print('Path found: {}'.format(reconst_path))
                return reconst_path

            # 현재 노드의 모든 이웃에 대해 수행함.
            for (m, weight) in self.get_neighbors(n):
                if m not in open_lst and m not in closed_lst:  # 현재 노드가 open_lst와 closed_lst 두 곳에 모두 존재하지 않는 경우
                    open_lst.add(m)                          #현재 노드를 open_lst에 추가함. 
                    par[m] = n
                    poo[m] = poo[n] + weight

               #그렇지 않으면 먼저 n을 방문한 다음 m을 방문하는 것이 더 빠른지 확인함.
                else:  
                    if poo[m] > poo[n] + weight:
                        poo[m] = poo[n] + weight
                        par[m] = n        # 만약 그렇다면 par 데이터와 poo 데이터를 업데이트 함.

                        if m in closed_lst:  # 노드가 closed_lst에 있으면 open_lst로 이동.
                            closed_lst.remove(m)
                            open_lst.add(m)

            open_lst.remove(n)  #open_lst에서 n을 제거하고 closed_lst에 추가함.(그것의 이웃은 모두 검사완료된 상태.)
            closed_lst.add(n)   

        print('Path does not exist!')
        return None

# B-F 최단경로
adjac_lis = {
    #corner : N11&12, N17&18, N27&28
    (12,31): [((12,28), 400)],
    (12,28): [((12,26), 755)],
    (12,26): [((12,24), 760)],
    (12,24): [((12,18), 370)],
    (12,18): [((12,21), 410)], #750 삭제
    (12,21): [((12,20), 350), ((9,21), 516)], #680 삭제
    (12,20): [((12,18), 453)], #668, 855 삭제
    (9,21): [((10,19), 460)],
    (10,19): [((12,18), 528)],
    (12,18): [((12,17),185), ((10,19), 500)], #910 삭제
    (12,17): [((12,16), 458)],
    (12,16): [((12,13), 525)],
    (12,13): [((12,12), 387)],
    (12,12): [((12,11), 415)],
    (12,11): [((12,12), 415)]
}
graph1 = Graph(adjac_lis)
graph1.a_star_algorithm((12,31), (10,19)) #출발지~목적지
graph1.a_star_algorithm((12,31), (12,13))
graph1.a_star_algorithm((12,31), (12,18))
