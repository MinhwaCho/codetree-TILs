# 삼성 SW 역량테스트 2022 하반기 오전 1번 문제
# 싸움땅
import sys
# sys.stdin = open("input.txt", "r")
input = sys.stdin.readline

# 초기설정
N,M,K = map(int,input().split())
maps = [list(map(int,input().split())) for _ in range(N)]
guns_loc = list() # [(x,y)]
guns_power = list() # [power]
points = [0]*M
players = dict() # {# : [d, s, gun_power]}
player_loc = list() # [(x,y)]
for _ in range(M):
    pi = list(map(int,input().split()))
    players[_] = [pi[2], pi[3], 0]
    player_loc.append((pi[0]-1, pi[1]-1))
# 상(0) 우(1) 하(2) 좌(3)
dr_x = [-1, 0, 1, 0]
dr_y = [0, 1, 0, -1]

for i in range(N):
    for j in range(N):
        if maps[i][j] > 0:
            guns_loc.append((i,j))
            guns_power.append(maps[i][j])
            maps[i][j] = 1

def get_gun(pla, pla_id, x, y):
    p_gun = pla[2]
    for g_i in range(len(guns_loc)):
        if guns_loc[g_i] == (x, y):
            m_gun = guns_power[g_i]
            if p_gun < m_gun:
                # 사용자 총 획득 -> guns_loc (-1,-1), players update
                players[pla_id][2] = m_gun
                guns_loc[g_i] = (-1, -1)
                # 사용자 총이 있다면, 바닥 총과 바꾸기
                if p_gun > 0:
                    guns_power[g_i] = p_gun
                    guns_loc[g_i] = (x, y)
                    p_gun = m_gun
# 라운드 시작
fight = False
for k in range(K):
# for k in range(2):
#     print(k,"round")
#     if k == 1:
#         print("GOGOo")
    # 1. 플레이어 순차 이동
    for player_id in range(M):
        player = players[player_id]
        si, sj = player_loc[player_id][0], player_loc[player_id][1]
        dr = player[0]
        ni, nj = si+dr_x[dr], sj+dr_y[dr]

        if (ni < 0 or ni >= N) or (nj < 0 or nj >= N): # 범위 밖인 경우
            dr = (dr + 2)%4     # 정반대 방향
            players[player_id][0] = dr
            ni, nj = si + dr_x[dr], sj + dr_y[dr]

        player_loc[player_id] = (ni, nj)

        fight = False
        for _pl_loc in range(len(player_loc)):
            # 다른 player가 있는 경우! 나 자신을 제외한
            if (ni, nj) == player_loc[_pl_loc] and _pl_loc != player_id:
                # 2-2. Fight
                fight = True
                o_player_id = _pl_loc#player_loc.index((ni, nj))
                o_player = players[o_player_id]
                flag = -1  # 0이면 player win, 1이면 o_player win
                # 2-2-1. 싸우기
                if (player[1] + player[2]) > (o_player[1] + o_player[2]):
                    flag = 0
                elif (player[1] + player[2]) == (o_player[1] + o_player[2]):
                    if player[1] > o_player[1]:
                        flag = 0
                    else:
                        flag = 1
                else:
                    flag = 1
                # print(players[3], player_id, o_player_id)
                # print(player_loc[player_id], player, player_loc[o_player_id], o_player)
                # print(player[1] + player[2], o_player[1] + o_player[2])
                # 2-2-2. 이긴 사람 # point 올리기, 총 비교 후 획득
                if flag == 0:
                    points[player_id] = abs((player[1] + player[2]) - (o_player[1] + o_player[2]))
                elif flag == 1:
                    points[o_player_id] = abs((player[1] + player[2]) - (o_player[1] + o_player[2]))
                else:
                    print("Error from the target_id");
                    break

                # 2-2-3. 진 사람
                if flag == 0:
                    target_player_id = o_player_id
                    t_si, t_sj = player_loc[target_player_id][0], player_loc[target_player_id][1]
                else:
                    target_player_id = player_id
                    t_si, t_sj = ni, nj
                # 총 내려 놓기:
                # p의 총 p = 0, gun_loc.append() gun_power.append()
                p_gun = players[target_player_id][2]
                if p_gun > 0:  # p의 총이 있다면
                    guns_loc.append((t_si, t_sj))
                    guns_power.append(p_gun)
                players[target_player_id][2] = 0
                # 한 칸 이동
                while True:
                    t_dr = players[target_player_id][0]
                    t_ni, t_nj = t_si + dr_x[t_dr], t_sj + dr_y[t_dr]

                    # 범위 밖 또는 다른 플레이어 존재한 경우
                    if (t_ni < 0 or t_ni >= N) or (t_nj < 0 or t_nj >= N):
                        # 다음에 빈칸 나올때까지 # 오른쪽 90도 회전 방향
                        t_dr = (t_dr + 1) % 4
                        players[target_player_id][0] = t_dr
                        continue
                    for pp in range(len(player_loc)):
                        if (t_ni, t_nj) == player_loc[pp] and pp != target_player_id:
                            continue
                    # 총이 있으면
                    if maps[t_ni][t_nj] > 0:
                        get_gun(players[target_player_id], target_player_id, t_ni, t_nj)
                    # 한 칸 이동 Update
                    player_loc[target_player_id] = (t_ni, t_nj)
                    break

                # 2-2-2. 이긴 사람 # point 올리기, 총 비교 후 획득
                if flag == 0:
                    # points[player_id] = abs((player[1] + player[2]) - (o_player[1] + o_player[2]))
                    get_gun(player, player_id, ni, nj)
                elif flag == 1:
                    # points[o_player_id] = abs((player[1] + player[2]) - (o_player[1] + o_player[2]))
                    get_gun(o_player, o_player_id, ni, nj)
                else:
                    print("Error from the target_id")
                    break
        # 2-1. 다른 player가 없는데,
        if fight==False and maps[ni][nj] > 0:  # 총이 있는 경우
            # player, return_gun
            get_gun(player, player_id, ni, nj)

print(' '.join(list(map(str,points))))
# print(player_loc)
# print(players)
# # print(guns_loc)
# # print(guns_power)
# for t,o in enumerate(zip(guns_loc, guns_power)):
#     print(t,o)