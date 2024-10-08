# 삼성 SW 역량테스트 2023 상반기 오전 1번 문제
# 포탑 부수기

import sys
from collections import deque

# sys.stdin = open("input.txt","r")
input = sys.stdin.readline

N,M,K = map(int,input().split())
maps = [list(map(int, input().split())) for _ in range(N)]
turrets = [] # (num, x, y, p, a, b) 공격력, 공격, 피해
ATT = 4
DAM = 5

cnt = 0
for i in range(N):
    for j in range(M):
        turrets.append((cnt, i, j, maps[i][j], -1, -1))
        cnt += 1

dx = [0,1,0,-1]
dy = [1,0,-1,0]
## 초기 설정

def choose_attacker(stage):
    min_power = 10000
    min_loc = (-1,-1)
    min_num = 100
    min_attack = 10000

    def change_min(x,y,c):
        return maps[x][y], (x,y), c, turrets[c][ATT]
    cnt = 0
    # 우선순위: 최근 공격(큰거) -> 행열합(큰거) -> 열 크기(큰): 약한거 고르기
    for i in range(N):
        for j in range(M):
            if maps[i][j] > 0:
                # target_num = i * N + j
                # print(target_num, cnt)
                if min_power > maps[i][j]:
                    min_power,min_loc,min_num,min_attack = change_min(i,j,cnt)
                elif min_power == maps[i][j]:# 공격력이 겹치면 # 최근 공격한게 약한 것 -> 선정
                    if min_attack < turrets[cnt][ATT]:
                        min_power, min_loc, min_num, min_attack = change_min(i, j, cnt)
                    # 행 열 합이 더 큰 포탑이 약한 것
                    if min_attack == turrets[cnt][ATT]:
                        if sum(min_loc) < sum((i,j)):
                            min_power, min_loc, min_num, min_attack = change_min(i, j, cnt)
                        # 열 값이 큰게 약한 것
                        elif (sum(min_loc) == sum((i, j))) and min_loc[1] < j:
                            min_power, min_loc, min_num, min_attack = change_min(i, j, cnt)
            cnt += 1
    return min_num, min_loc[0], min_loc[1], min_power+N+M, stage, turrets[min_num][DAM]

def choose_damager(stage):
    max_power = -1
    max_loc = (10000, 10000)
    max_num = -1
    max_damage = -1

    def change_max(x,y,c):
        return maps[x][y], (x,y), c, turrets[c][DAM]
    cnt = 0
    # 우선순위: 최근 공격(작은거) -> 행열합(작은거) -> 열 크기(작은거) 바꿔야함!
    for i in range(N):
        for j in range(M):
            if maps[i][j] > 0:
                if max_power < maps[i][j]:
                    max_power, max_loc, max_num, max_damage = change_max(i, j, cnt)
                elif max_power == maps[i][j]:  # 공격력이 겹치면 # 오래된 공격한게 강한 것 -> 선정
                    if max_damage > turrets[cnt][DAM]:
                        max_power, max_loc, max_num, max_damage = change_max(i, j, cnt)
                    # 행 열 합이 더 작은 포탑이 강한 것
                    if max_damage == turrets[cnt][DAM]:
                        if sum(max_loc) < sum((i, j)):
                            max_power, max_loc, max_num, max_damage = change_max(i, j, cnt)
                        # 열 값이 작은게 강한 것
                        elif (sum(max_loc) == sum((i, j))) and max_loc[1] > j:
                            max_power, max_loc, max_num, max_damage = change_max(i, j, cnt)
            cnt += 1
    return max_num, max_loc[0], max_loc[1], max_power, turrets[max_num][ATT], stage

def update(turret):
    num,x,y,p,a,b = turret
    if p < 0: p = 0
    turrets[num] = turret
    maps[x][y] = p

def get_ni(i, j, di, dj):
    ni = i+di
    nx = i + di
    ny = j + dj

    if nx < 0: nx = N-1
    elif nx >= N: nx = 0

    if ny < 0: ny = M-1
    elif ny >= M: ny = 0

    return nx,ny
    # if ni < 0: return max-1
    # elif ni >= max: return 0
    # else: return ni

def find_shortest_path(at_tu, da_tur):
    if at_tu == (7, 1, 3, 9, 2, 1):
        print("debug")
    start_x, start_y = at_tu[1], at_tu[2]
    end_x, end_y = da_tur[1], da_tur[2]

    visited = [[False]*M for _ in range(N)]
    for i in range(N):
        for j in range(M):
            if maps[i][j] < 0: visited[i][j] = True

    queue = deque()
    queue.append([start_x,start_y, [(start_x,start_y)]])
    sh_path = [0]*10000

    visited[start_x][start_y] = True
    while queue:
        sx, sy, path = queue.popleft()
        if len(path)>0 and sx==end_x and sy==end_y:
            if len(sh_path) > len(path):
                sh_path = path
            break

        for i in range(4): # 우/하/좌/상의 우선순위대로
            # nx = get_ni(sx, dx[i], N)
            # ny = get_ni(sy, dy[i], M)
            nx, ny = get_ni(sx, sy, dx[i], dy[i])
            if maps[nx][ny] > 0 and not visited: # 갈 수 있는 길로 가기
                queue.append([nx, ny, path+[(nx,ny)]])
                visited[nx][ny] = True
    return sh_path
# find_shortest_path((1, 0, 1, 9, 0, -1), (11, 2, 3, 26, 0, 0))

def laser(at_tu, da_tur):

    shortest_path = find_shortest_path(at_tu, da_tur)
    # print("최단경로",at_tu, da_tur,shortest_path)
    if len(shortest_path)<10000: # 최단경로가 있는 경우
        # print(shortest_path) # 공격자 반피해 반피해 ... 피해자 까지 -> [(0, 1), (0, 2), (0, 3), (1, 3), (2, 3)]
        # 공격 대상은 공격자의 공격력만큼 피해
        update((da_tur[0],da_tur[1],da_tur[2], da_tur[3]-at_tu[3],da_tur[4],k))
        # 경로 피해 대상자는 공격력반만큼 피해
        for i in range(1, len(shortest_path[:-1])):
            target_loc = shortest_path[i]
            target_num = target_loc[0]*N + target_loc[1]
            target_turr = turrets[target_num]
            update((target_turr[0],target_turr[1],target_turr[2], target_turr[3]-(at_tu[3] // 2),target_turr[4],k))
        return True
    else:
        return False

def boom(at_tur, da_tur):
    # 공격 대상은 공격자의 공격력만큼 피해
    kill_power = at_tur[3]
    update((da_tur[0], da_tur[1], da_tur[2], da_tur[3] - kill_power, da_tur[4], k))
    # 경로 피해 대상자는 공격력반만큼 피해
    da_num, da_x, da_y, da_p, da_a, da_b = da_tur
    condition = []
    for i in range(4):
        condition.append(get_ni(da_x, da_y, dx[i], dy[i]))
    for i,j in [(1,1),(-1,-1),(1,-1),(-1,1)]:
        condition.append(get_ni(da_x, da_y, i, j))
    # print("Target Condition")
    for nx,ny in condition:
        if maps[nx][ny] > 0:
            # print(nx,ny)
            target_num = (nx * N) + ny
            target_turr = turrets[target_num]
            update((target_turr[0], target_turr[1], target_turr[2], target_turr[3] - (kill_power // 2), target_turr[4], k))

def attack(at_tur, da_tur):
    if laser(at_tur, da_tur):
        return
    boom(at_tur, da_tur)
    # print("attack")

def maintaince(stage):
    for turret in turrets:
        # 부서지면 pass
        if maps[turret[1]][turret[2]] == 0: continue
        # 공격과 무관했을 경우
        if turret[ATT] != stage and turret[DAM] != stage:
            update((turret[0], turret[1], turret[2], turret[3]+1, turret[4], turret[5]))


## 시뮬레이션
for k in range(K):
    # print(k, "stage start >>>")
    # print(maps)
    # print(turrets)
    # 종료 조건
    if sum([sum(maps[i]) for i in range(N)]) == 1: break

    # 1. 공격자, 피해자 선정
    attacker = choose_attacker(k)
    damager = choose_damager(k)
        # update
    update(attacker)
    update(damager)

    # print("공격자, 피해자 선정 후")
    # print(maps)
    # print(turrets)
    # print('공격자', attacker)
    # print('피해자', damager)

    # 2. 공격
    attack(attacker, damager)
    #
    # print("공격 후")
    # print(maps)
    # print(turrets)

    # # 3. 정비
    maintaince(k)

    # print(k,"stage 끝")
    # print(maps)
    # print(turrets)

max_power = 0
for i in range(N):
    max_power = max(max_power, max(maps[i]))
print(max_power)