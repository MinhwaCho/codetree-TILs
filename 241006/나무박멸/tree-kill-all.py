# 삼성 SW 역량테스트 2022 상반기 오후 2번 문제
# 나무 박멸
import sys
input = sys.stdin.readline
N,M,K,C = map(int, input().split())
maps = [list(map(int,input().split())) for i in range(N)]
# N,M,K,C = 5,2,2,1
# maps = [
#     [0,0,0,0,0],
#     [0,30,23,0,0],
#     [0,0,-1,0,0],
#     [0,0,17,46,77],
#     [0,0,0,12,0]
# ]

killer_maps = [[0]*N for i in range(N)]
killer_maps[N//2][N//2] = -1
# killer_maps = [
#     [0,1,0,0,0],
#     [0,0,0,0,0],
#     [0,0,0,0,0],
#     [0,0,0,0,0],
#     [0,0,0,0,0]
# ]


total_result = 0

for m in range(M):
    # print(">>>>", m)
    # print(maps)

    # 제초제 하나씩 없애기
    for i in range(N):
        for j in range(N):
            if killer_maps[i][j] > 0:
                killer_maps[i][j] -= 1
    # print(killer_maps)

    # 1. 나무 성장
    for i in range(N):
        for j in range(N):
            if i == N//2 and j == N//2: continue
            adj = 0 
            if maps[i][j]: # 나무가 있다면 인접 칸 수 구하기
                for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                    ci,cj = di+i, dj+j
                    if 0<=ci<N and 0<=cj<N and maps[ci][cj]>0: # 범위내, 나무가 있고
                        adj += 1
                maps[i][j] += adj # 성장

    # 2. 번식
    # import copy
    # new_maps = copy.deepcopy(new_maps)
    new_maps = [mapss[:] for mapss in maps]
    for i in range(N):
        for j in range(N):
            if i == N//2 and j == N//2: continue
            reproduce = 0
            if maps[i][j]: # 나무가 있다면
                for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                    ci,cj = di+i, dj+j
                    # 조건: 범위내, 다른 나무 없고, 제초제가 없고
                    if 0<=ci<N and 0<=cj<N and maps[ci][cj]==0 and killer_maps[ci][cj]==0:
                        reproduce += 1
                # 번식
                for di,dj in ((-1,0),(1,0),(0,-1),(0,1)):
                    ci,cj = di+i, dj+j
                    if 0<=ci<N and 0<=cj<N and maps[ci][cj]==0 and killer_maps[ci][cj]==0:
                        new_maps[ci][cj] += (maps[i][j]//reproduce)
    maps = new_maps # map update
    # print(maps)

    # 3. 제초제 뿌릴 위치 선정
    choose_killer_loc = [[0]*N for i in range(N)]
    for i in range(N):
        for j in range(N):
            if i == N//2 and j == N//2: continue
            total_kill = 0
            if maps[i][j]: # 나무가 있다면
                total_kill += maps[i][j]
                for di,dj in ((-1,-1),(1,-1),(-1,1),(1,1)):
                    for k in range(1, K+1): # 대각선 범위만큼
                        ci,cj = (di*k)+i, (dj*k)+j
                        # 조건: 범위내, 나무가 있다
                        if 0<=ci<N and 0<=cj<N and maps[ci][cj] > 0:
                            total_kill += maps[ci][cj]
                        # 조건: 벽 또는 나무가 없을 경우 거기까지, => 대각선 끝
                        if (ci<0 or ci>=N) or (cj<0 or cj>=N) or maps[ci][cj] < 0:
                            break
            choose_killer_loc[i][j] = total_kill
    # print(choose_killer_loc)

    target_loc = (0,0)
    max_kill = 0
    for j in range(N):
        for i in range(N):
            if choose_killer_loc[i][j] > max_kill:
                max_kill = choose_killer_loc[i][j]
                target_loc = (i,j)
    # print(target_loc)

    # 4. 제초제 작업 진행
    new_maps = [mapss[:] for mapss in maps]
    for i in range(N):
        for j in range(N):
            if i == N//2 and j == N//2: continue
            if i == target_loc[0] and j == target_loc[1]:
                total_result += maps[i][j]
                killer_maps[i][j] = (C+1)
                new_maps[i][j] = 0
                for di,dj in ((-1,-1),(1,-1),(-1,1),(1,1)):
                    for k in range(1, K+1): # 대각선 범위만큼
                        ci,cj = (di*k)+i, (dj*k)+j
                        # 조건: 범위내, 나무가 있다
                        if 0<=ci<N and 0<=cj<N:
                            killer_maps[ci][cj] = (C+1)
                            if maps[ci][cj] > 0:
                                total_result += maps[ci][cj]
                                new_maps[ci][cj] = 0
                        # 조건: 벽 또는 나무가 없을 경우 거기까지, => 대각선 끝
                        if (ci<0 or ci>=N) or (cj<0 or cj>=N) or maps[ci][cj] < 0:
                            break
    maps = new_maps

print(total_result)