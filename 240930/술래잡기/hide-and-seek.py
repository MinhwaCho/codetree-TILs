import sys
from collections import deque
input = sys.stdin.readline



n,m,h,k = map(int,input().split())
runner_list = [list(map(int,input().split())) for i in range(m)]
tree_list = [list(map(int,input().split())) for i in range(h)]
# n,m,h,k = 5,3,1,2
# runner_list = [[2, 4, 1], [1, 4, 2], [4, 2, 1]]
# tree_list = [[2, 4]]
runner_list_ = []
for runner in runner_list:
    runner_list_.append([runner[0]-1, runner[1]-1, runner[2]])
runner_list = runner_list_
tree_list_ = []
for tree in tree_list:
    tree_list_.append([tree[0]-1, tree[1]-1])
tree_list = tree_list_

runner_1 = [[0,1],[0,-1]]
runner_2 = [[1,0],[-1,0]]

def move(loc, vol, dir):
    x, y = loc[0], loc[1]
    dx = vol*dir[0]
    dy = vol*dir[1]
    x = x + dx; y = y + dy
    return [x,y]


def distance(catcher, runner):
    return abs(catcher[0]-runner[0]) + abs(catcher[1]-runner[1])
def have_to_run(catcher, runner):
    dist = distance(catcher, runner)
    if dist <= 3: return True
    else: return False

def iswall(loc, dx, dy):
    x,y = loc[0], loc[1]
    if x+dx < 0 or x+dx > n-1:
        return True
    if y+dy < 0 or y+dy > n-1:
        return True
    return False

def move_runner(catcher_loc, runner_loc, runner_dir):
    runner_dict = {
        '0': [0,-1],
        '1': [0,1],
        '2': [1,0],
        '3': [-1,0]
    }
    dx, dy = runner_dict[str(runner_dir)][0], runner_dict[str(runner_dir)][1]
    runner_xy = move(runner_loc, 1, [dx,dy])
    
    # 벽에 마주치면 direction 반대로
    if iswall(runner_xy, dx, dy): # 벽에 마주치면 direction 반대로
            if runner_dir == 1: runner_dir = 0
            elif runner_dir == 0: runner_dir = 1
            elif runner_dir == 2: runner_dir = 3
            elif runner_dir == 3: runner_dir = 2
    runner_xy = move(runner_loc, 1, runner_dict[str(runner_dir)])
    if runner_xy != catcher_loc: # 술래가 없으면 움직이기
       return runner_xy+[runner_dir]
    else:
        return runner_loc+[runner_dir]

def is_catch(catcher_loc, runner_loc, ey_dx, ey_dy, tree_list):
    catcher_x, catcher_y = catcher_loc[0], catcher_loc[1]
    while catcher_x > 0 and catcher_x < n and catcher_y > 0 and catcher_y < n:
        if runner_loc == [catcher_x, catcher_y]:
            for tree in tree_list:
                if tree == [catcher_x, catcher_y]: return False
            return True
        catcher_x += ey_dx
        catcher_y += ey_dy
    return False


catcher_direction_1 = deque([[-1,0],[0,1],[1,0],[0,-1]])
catcher_direction_2 = deque([[1,0],[0,1],[-1,0],[0,-1]])
catcher_direction_xy = catcher_direction_1.copy()
catcher_loc = [n//2, n//2]
answer = 0
# catcher_volume = 1

t = 0
k_turn = 0
while True:
    # 첫번쨰 도망자 움직이기
    # if t % 2 == 0:
    # print("runner turn----------------------------------------")
    for i in range(len(runner_list)):
        runner = runner_list[i].copy()
        runner_x, runner_y, runner_dir = runner[0], runner[1], runner[2]
        if have_to_run(catcher_loc, [runner_x, runner_y]): # 도망자와 술래 거리 3이하인 경우 도망
            runner = move_runner(catcher_loc, [runner_x, runner_y], runner_dir)
        runner_list[i] = runner
    # print(runner_list)

    
    # 두번째 술래 움직이고 술래잡기
    # else:
    # 먼저 술래 움직이기
    # print("catcher turn----------------------------------------")
    if catcher_loc == [0,0]: 
        catcher_direction = False
        k_turn = 1
        catcher_direction_xy = catcher_direction_2.copy()
        # print("catcher direction change")
    elif catcher_loc == [n//2, n//2]:
        catcher_direction = True
        k_turn = 0
        catcher_volume = 1
        catcher_direction_xy = catcher_direction_1.copy()
        # print("catcher direction change")


    if catcher_direction:
        catcher_loc = move(catcher_loc, catcher_volume, catcher_direction_xy[0])
        catcher_direction_xy.rotate(-1)
        if k_turn % 2 == 1:
            catcher_volume += 1
        if catcher_volume == n:
            catcher_volume = n-1
    else:
        catcher_loc = move(catcher_loc, catcher_volume, catcher_direction_xy[0])
        catcher_direction_xy.rotate(-1)
        if catcher_volume == n-1 and catcher_loc == [n-1,0]:
            catcher_volume = n-1
        elif k_turn % 2 == 1:
            catcher_volume -= 1
    # print(catcher_loc, k_turn, k)

    # 술래잡기
    catch_runner_index = []
    catch_runner = []
    catcher_eye_dx,catcher_eye_dy = catcher_direction_xy[0][0], catcher_direction_xy[0][1]
    for i in range(len(runner_list)):
        runner_loc = runner_list[i][:2]
        if is_catch(catcher_loc,runner_loc,catcher_eye_dx,catcher_eye_dy,tree_list):
            catch_runner_index.append(i)
    # print((t+1), "turn")
    # print("잡은 술래 수", len(catch_runner_index), runner_list)
    answer += (t+1)*len(catch_runner_index)
    ## 도망자 잡은 후 도망자 리스트에서 없애기
    for i in range(len(runner_list)):
        if i not in catch_runner_index: catch_runner.append(runner_list[i])
    runner_list = catch_runner
    # print("술래 수", runner_list)
    
    # 술래 움직이기 용이하기 위한 변수 k_turn
    k_turn += 1


    t += 1
    
    if t == k: break
    if len(runner_list) == 0: break

print(answer)