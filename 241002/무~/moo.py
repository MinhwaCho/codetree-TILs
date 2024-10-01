N=int(input())

s = [["m","o","o"]]
def divide_conquer(ind):
    return s[ind-1] + ["m"] + ["o"]*(ind+2) + s[ind-1]
for i in range(1, N+1):
    s.append(divide_conquer(i))
print(s[N][N-1])