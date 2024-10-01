N=int(input())

# s = [["m","o","o"]]
# def divide_conquer(ind):
#     return s[ind-1] + ["m"] + ["o"]*(ind+2) + s[ind-1]
# for i in range(1, N+1):
#     s.append(divide_conquer(i))
# print(s[N][N-1])

def divide_conquer(x):
    # if x == N: return
    if x == 0:
        return ["m","o","o"]
    else:
        el = divide_conquer(x-1)
        return el + ["m"] + ["o"]*(x+2) + el
print(divide_conquer(N)[N-1])