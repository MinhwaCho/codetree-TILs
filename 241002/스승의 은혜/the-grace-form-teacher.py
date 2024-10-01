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
# N,B = 5,24
# P_list = [4,2,8,6,12]
# S_list = [2,0,1,3,5]

student = [True]*N
price = sum(P_list)+sum(S_list)
result = 0


def calculate_payment(s_list, all_price):
    res = all_price
    for i in range(N):
        price = all_price
        if s_list[i]:
            price -= (P_list[i] + S_list[i])
            price += ((P_list[i]//2) + S_list[i])
            if price <= B:
                res = price
                return res
    return res


price = calculate_payment(student, price)
def dfs(ind, payment):
    global student
    global result

    if payment <= B:
        result =  max(result, sum(student))
        return
    else:
        for i in range(N-1, ind-1, -1):
            if student[i]:
                student[i] = False
                payment = 0
                for i in range(N):
                    if student[i]:
                        payment += (P_list[i] + S_list[i])
                payment = calculate_payment(student, payment)
                # print(student, payment)
                dfs(i, payment)
                student[i] = True
dfs(0, price)
print(result)