# 삼성 SW 역량테스트 2022 상반기 오후 1번 문제
# 꼬리잡기놀이
from collections import deque
import sys

# N,M,K = 7,2,2
# maps = [
#     [3,2,1,0,0,0,0],
#     [4,0,4,0,2,1,4],
#     [4,4,4,0,2,0,4],
#     [0,0,0,0,3,0,4],
#     [0,0,4,4,4,0,4],
#     [0,0,4,0,0,0,4],
#     [0,0,4,4,4,4,4]
# ]
input = sys.stdin.readline
N,M,K = map(int, input().split())
maps = [list(map(int,input().split())) for i in range(N)]

direction_1 = [(0,1),(1,0),(-1,0)]
direction_2 = [(0,-1),(1,0),(-1,0)]

dire = [(0,1),(0,-1),(1,0),(-1,0)]

##
header = []
for i in range(N):
    for j in range(N):
        if maps[i][j] == 1:
            header.append([1,(i,j)])
# print(header) # [[1, (0, 2)], [1, (1, 5)]]
##

def move_step():
    next_maps = [[-1]*N for i in range(N)]
    
    def dfs(head):
        find_dir = [(0,1),(0,-1),(1,0),(-1,0)]

        if head[0] == 1: 
            direction = direction_1
        else: 
            direction = direction_2

        q = [head[1]]
        visited.append(head[1])

        # print(q) # (0,2)
        while q:
            # print(q)
            _q = q.pop()
            r,c = _q[0], _q[1]
            for i in range(len(find_dir)):
                if -1<r+find_dir[i][0]<N and -1<c+find_dir[i][1]<N:
                    t = maps[r+find_dir[i][0]][c+find_dir[i][1]]
                    if (r+find_dir[i][0], c+find_dir[i][1]) not in visited:
                        if t == 2 or t == 3:
                            q.append((r+find_dir[i][0],c+find_dir[i][1]))
                            visited.append((r+find_dir[i][0],c+find_dir[i][1]))

            if maps[r][c] == 1:
                for d in range(len(direction)):
                    dx, dy = r+direction[d][0], c+direction[d][1]
                    if -1<dx<N and -1<dy<N:
                        if head[0] == 1 and maps[dx][dy] == 4:
                            next_maps[dx][dy] = 1
                            new_head_loc = (dx,dy)
                        elif head[0] !=1 and maps[dx][dy] == 2:
                            next_maps[dx][dy] = 1
                            new_head_loc = (dx,dy)
            elif maps[r][c] == 2:
                for d in range(len(direction)):
                    dx, dy = r+direction[d][0], c+direction[d][1]
                    if -1<dx<N and -1<dy<N:
                        if head[0] == 1 and maps[dx][dy] == 1:
                            next_maps[dx][dy] = 2
                            head.append((dx,dy))
                            break
                        elif maps[dx][dy] == 2:
                            next_maps[dx][dy] = 2
                            head.append((dx,dy))
                            break
                        elif head[0] !=1 and maps[dx][dy] == 3:
                            next_maps[dx][dy] = 2
                            head.append((dx,dy))
                            break
            elif maps[r][c] == 3:
                for d in range(len(direction)):
                    dx, dy = r+direction[d][0], c+direction[d][1]
                    if -1<dx<N and -1<dy<N:
                        if head[0] == 1 and maps[dx][dy] == 2:
                            next_maps[dx][dy] = 3
                            next_maps[r][c] = -1
                            head.append((dx,dy))
                        elif head[0] !=1 and maps[dx][dy] == 4:
                            next_maps[dx][dy] = 3
                            head.append((dx,dy))
        return new_head_loc

    for k in range(len(header)):
        visited = []
        header[k] = header[k][:2]
        head = header[k]
        new_head_loc = dfs(head)
        header[k][1] = new_head_loc # head 1 update
        # print(header[k])
    return next_maps


round_dir = deque([(0,1), (-1,0), (0,-1), (1,0)])
# round_1 = [[0,1]]+[(i,0) for i in range(N)]
# round_2 = [[-1,0]]+[(0,i) for i in range(N)]
# round_3 = [[0,-1]]+[(i,0) for i in range(N-1,-1,-1)]
# round_4 = [[1,0]]+[(0,i) for i in range(N-1,-1,-1)]
round_1 = [(i,0) for i in range(N)]
round_2 = [(N-1,i) for i in range(N)]
round_3 = [(i,N-1) for i in range(N-1,-1,-1)]
round_4 = [(0,i) for i in range(N-1,-1,-1)]
round_all = deque(round_1+round_2+round_3+round_4)

k = 0
# K = 2
result = 0
while k != K:
    # print("Round",k)
    # 1. 움직임
    next_step = move_step()
    # print(maps)
    # print(next_step)
    for i in range(N):
        for j in range(N):
            if maps[i][j] == 0: 
                next_step[i][j] = 0
            elif next_step[i][j] == -1:
                next_step[i][j] = 4
    # print(next_step)
    maps = next_step

    # 2. 공 던짐
    round_dx, round_dy = round_dir[0][0], round_dir[0][1]
    # print(round_all[0])
    # print(round_dx, round_dy)
    
    # 3. 공 맞는지 확인 및 점수 update
    # 4. 공 맞은 팀 방향 전환
    score = 0
    for h in range(len(header)):
        # print(header[h]) # [1, (1, 2), (0, 2), (0, 1)]
        team = header[h][1:]
        for i in range(N):
            ball_x, ball_y = round_all[0][0]+(round_dx*i), round_all[0][1]+(round_dy*i)
            ind = 1
            if (ball_x, ball_y) in team:
                for j in range(len(team)):
                    if team[j] == (ball_x, ball_y): break
                    ind += 1
                # print(ind, (ball_x, ball_y), team)
                score += (ind*ind)
                if header[h][0] == 1:
                    header[h][0] = 2
                elif header[h][0] == 2:
                    header[h][0] = 1
                break
    # print(score)
    result += score


    if k % N == 0 and k > 0:
        round_dir.rotate(-1)
    round_all.rotate(-1)
    ##
    k+=1

print(result)