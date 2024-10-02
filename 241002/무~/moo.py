import sys
input = sys.stdin.readline

N = int(input())

def cal_length(k):
    if k == 0: return 3
    return cal_length(k-1)*2 + (k+3)

def d_c(k, n):
    if k == 0:
        if n == 1: return "m"
        else: return "o"

    else:
        left_length = cal_length(k-1)
        middle_length = k+3
        if n <= left_length:
            return d_c(k-1, n)
        elif n > (left_length + middle_length):
            return d_c(k-1, n - left_length - middle_length)
        else: # 중앙
            if n == left_length + 1: return "m"
            else: return "o"

# k가 포함되어 있는 S(k) 구하기
k = 0
while cal_length(k) < N:
    k += 1

res = d_c(k, N)
print(res)