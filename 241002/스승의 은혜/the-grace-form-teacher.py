# 스승의 은혜 - 실버3

#스승 N -> 학생: 예산 B
# 학생 i 선물가격 P(i), 배송비 S(i)
# 선생님 선물 하나 반값 할인 쿠폰
# 선물 간으한 학생 최대 명수

import sys
input = sys.stdin.readline
N,B = map(int,input().split())
P_list, S_list = [], []
for i in range(N):
    inp = list(map(int, input().split()))
    P_list.append(inp[0]); S_list.append(inp[1])


total_cost = [(P_list[i]+S_list[i]) for i in range(N)]
total_cost.sort()
# print(total_cost)

def apply_coupon(ind):
    t_list = []
    for i in range(N):
        if i == ind: t_list.append((P_list[i]//2)+S_list[i]); continue
        t_list.append(P_list[i]+S_list[i])
    return t_list

max_count = 0
for i in range(N):
    max_student_count = 0
    price_count = 0

    total_coupon_cost = apply_coupon(i)
    total_coupon_cost.sort()
    # print(total_coupon_cost)

    for j in range(N):
        if price_count > B:
            break
        price_count += total_coupon_cost[j]
        max_student_count += 1
    
    # print(price_count, max_student_count-1)
    max_count = max(max_count, max_student_count-1)

print(max_count)