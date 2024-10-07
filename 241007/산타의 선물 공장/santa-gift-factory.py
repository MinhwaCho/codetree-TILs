# 삼성 SW 역량테스트 2022 하반기 오전 2번 문제
# 산타의 선물 공장

from collections import deque
import sys
input = sys.stdin.readline

Q = int(input())
belt = list() # belt_id
box = dict() # box_id: box_weight
belt_box = dict() # belt_id: deque([box_id, ...])
N,M = 0,0

# Q = 1
# belt = list([0, 1, 2])
# box = {10: 30, 12: 30, 20: 20, 15: 20, 14: 10, 19: 18, 22: 17, 25: 15, 16: 25, 17: 11, 21: 14, 18: 17}
# # belt_box = {0: deque([10, 12, 20, 15]), 1: deque([14, 19, 22, 25]), 2: deque([16, 17, 21, 18])}
# # belt_box = {0: deque([12, 20, 15, 10]), 1: deque([19, 22, 25]), 2: deque([17, 21, 18])}
# # belt_box = {0: deque([12, 20, 15, 10]), 1: deque([19, 25]), 2: deque([17, 21, 18])}
# belt_box = {0: deque([12, 20, 15, 10]), 1: deque([19, 25]), 2: deque([17, 21])}
# # belt_box = {0: deque([12, 20, 15, 10, 17, 21]), 1: deque([19, 25]), 2: []}

# N,M = 12, 3

for q in range(Q):
    f = list(map(int,input().split()))
    # f = "100 12 3 10 12 20 15 14 19 22 25 16 17 21 18 30 30 20 20 10 18 17 15 25 11 14 17"
    # f = "500 3"
    # f = list(map(int,f.split()))

    # 1. 공장 설립
    if f[0] == 100:
        N,M = f[1], f[2]
        belt = deque()
        belt.extend(list(range(M)))
        f = f[3:]
        for i in range(N): box[f[i]] = 0
        for j in range(N):  box[list(box.keys())[j]] = f[N+j]
        # 벨트마다 물건 올리기
        much = N//M
        for i in range(M):
            belt_box[belt[i]] = deque()
            for j in range(i*much, (i+1)*much):
                belt_box[belt[i]].append(list(box.keys())[j])
    # 2. 물건 하차
    elif f[0] == 200:
        # print("물건 하차")
        # print(box)
        weight = f[1]
        result = 0
        for m in belt:
            if box[belt_box[m][0]] <= weight:
                result += box[belt_box[m][0]]
                belt_box[m].popleft()
            else:
                t = belt_box[m].popleft()
                belt_box[m].append(t)
        print(result)
    # 3. 물건 제거
    elif f[0] == 300:
        r_id = f[1]
        for m in belt:
            if r_id in belt_box[m]:
                belt_box[m].remove(r_id)
                # while True:
                #     box_id = belt_box[m].popleft()
                #     if box_id == r_id: # 상자 맨앞으로 나오면, 제거
                #         break
                #     else: # 앞 상자 뒤로이동
                #         belt_box[m].append(box_id)
                print(r_id)
                r_id = -1
                break
        if r_id != -1:
            print("-1")
    # 4. 물건 확인
    elif f[0] == 400:
        f_id = f[1]
        for m in belt:
            if f_id in belt_box[m]:
                while True:
                    box_id = belt_box[m].popleft()
                    if box_id == f_id: # 상자 맨앞으로 나오면,
                        # belt_box[m].append(box_id)
                        belt_box[m].insert(0,box_id)
                        f_id = -1
                        print(m+1) # 벨트 번호 출력!!
                        break
                    else: # 앞 상자 뒤로이동
                        belt_box[m].append(box_id)
                    # box_id = belt_box[m][0]
                    # if box_id == f_id:
                    #     belt_box[m].popleft()
                    #     print(m+1) # 벨트 번호 출력!!
                    #     f_id = -1
                    #     break
                    # else:
                    #     t = belt_box[m].popleft()
                    #     belt_box[m].append(t)
        if f_id != -1:
            print("-1")
    # 5. 벨트 고장
    elif f[0] == 500:
        b_num = f[1]-1
        searching_belt = deque(belt)
        if b_num not in belt: # 고장이 이미 나있다면
            print("-1")
        else:
            while True:
                belt_num = searching_belt[0]
                if belt_num == b_num:
                    # print(searching_belt[1])
                    break
                searching_belt.rotate(-1)
            target_belt = searching_belt[1] # 옆 벨트 번호
            belt.remove(b_num) # belt 고장
            # 옆 벨트에 상자 옮기기
            belt_box[target_belt].extend(belt_box[b_num])
            belt_box[b_num] = []
            print(b_num+1) # 고장 처리 후 벨트 번호 출력
    
    # print(belt_box) # 확인용