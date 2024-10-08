# 삼성 SW 역량테스트 2022 하반기 오후 1번 문제
# 코드트리 빵
import sys
from collections import deque
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline

# 초기설정
N,M = map(int, input().split())
maps = [list(map(int,input().split())) for _ in range(N)]
people = []
stores = []
base_camps = []
for _ in range(M):
    p = list(map(int, input().split()))
    people.append((_, -1,-1, p[0]-1, p[1]-1, False))
    stores.append((p[0]-1, p[1]-1))

for i in range(N):
    for j in range(N):
        if maps[i][j] == 1: base_camps.append((i,j))
for x,y in stores:
    maps[x][y] = 2

store_visited = []
dr_x = [-1, 0, 0, 1]
dr_y = [0, -1, 1, 0]
## 초기 설정
## 시작
def in_range(x, y):
    return 0<=x<N and 0<=y<N

def shortest_path(start_x, start_y, end_x, end_y):
    visited = [[False]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            if maps[i][j] < 0: # 지나갈 수 없는 길이면 visited True 처리
                visited[i][j] = True

    queue = deque()
    queue.append((start_x, start_y, [(start_x, start_y)]))

    while queue:
        sx, sy, path = queue.popleft()
        if sx == end_x and sy == end_y:
            return path[1:]

        for i in range(4):
            nx, ny = sx+dr_x[i], sy+dr_y[i]

            if in_range(nx,ny) and not visited[nx][ny]:
                queue.append((nx,ny,path+[(nx,ny)]))
                visited[nx][ny] = True

def people_update(p):
    num_, px_, py_, x_, y_, a_ = p
    people[num_] = p

    # print("사람 업데이트")
    # print(people)

# 사람 정보의 a를 보고 편의점 map 음수처리
# 사람 위치와 베이스캠프 위치가 같을 경우 베이스캠프 map 음수처리
def update_map():
    for p_ in people:
        num_, px_, py_, x_, y_, a_ = p_
        if a_:
            maps[x_][y_] = -2
        if (px_, py_) in base_camps:
            maps[px_][py_] = -1

# 편의점과 가장 가까운 베이스캠프 고르기 (갈 수 없는 길 잘 보고 하기)
def choose_basecamp(end_x, end_y):
    target_basecamps = []
    # 지나갈 수 있는 베이스캠프
    for bx, by in base_camps:
        if maps[bx][by] == 1:
            target_basecamps.append((bx,by))
    # for i in range(N):
    #     for j in range(N):
    #         if maps[i][j] == 1: # 지나갈 수 있는 베이스캠프
    #             target_basecamps.append((i,j))

    s_path = []
    for tx, ty in target_basecamps:
        visited = [[False] * N for _ in range(N)]
        for i in range(N):
            for j in range(N):
                if maps[i][j] < 0:  # 지나갈 수 없는 길이면 visited True 처리
                    visited[i][j] = True
        i_path = []
        queue = deque()
        queue.append([tx, ty, [(tx,ty)]])
        while queue:
            sx, sy, path = queue.popleft()
            if sx == end_x and sy == end_y:
                i_path = path
                break
            for i in range(4):
                nx, ny = sx + dr_x[i], sy + dr_y[i]
                if in_range(nx, ny) and not visited[nx][ny]:
                    queue.append([nx, ny, path+[(nx,ny)]])
                    visited[nx][ny] = True

        if len(i_path)>0 and (len(s_path) == 0 or len(s_path) > len(i_path)):
            s_path = i_path

    return s_path[0]

# 시뮬레이션
t = 0
while True:
# for _ in range(3):
#     print(t,"round >>>>")
    if len(store_visited) == M: break

    # 1. t 만큼의 사람 이동
    for p in people:
        num, px, py, x, y, a = p
        if px==-1 and py==-1: # 아직 사람이 나오지 않았으면
            continue
        if a: # 편의점에 도착했으면 이동 x
            continue

        # print("사람 이동", num)
        s_path = shortest_path(px, py, x, y) # [(1, 0), (2, 0), (2, 1), (2, 2)]
        nx,ny = s_path[0]
        # print("다음 위치", s_path, nx,ny)

        # 편의점 도착!
        if nx == x and ny == y:
            people_update((num, nx, ny, x, y, True))
            store_visited.append((nx,ny))
            # print("편의점 도착", people[num], store_visited)
        else:
            people_update((num, nx, ny, x, y, False))

    update_map() # 사람 정보의 a를 보고 편의점 map 음수처리
                # 사람 위치와 베이스캠프 위치가 같을 경우 베이스캠프 map 음수처리
    # print(maps)

    # 2. t 사람 위치 설정
    if t <= M-1:
        # print("사람 위치 설정")
        p = people[t]
        num, px, py, x, y, a = p

        bx,by = choose_basecamp(x,y)
        # print("베이스캠프", bx,by)

        people_update((t, bx, by, x, y, a))
    update_map()
    t += 1
print(t)