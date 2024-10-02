import sys
input = sys.stdin.readline
N = int(input())
check_list = [int(input()) for i in range(N)]

target_ind = 0
for i in range(N-1):
    if check_list[i] > check_list[i+1]: 
        target_ind = i+1

# print("target index: ", target_ind)
arr = check_list[:target_ind]
# print("Array:", arr)

cnt = 0
target_num = check_list[target_ind]
for i in range(len(arr)-1,-1,-1):
    if arr[i] > target_num:
        if i >= 1 and arr[i] == arr[i-1]: 
            continue
        else:
            cnt += 1
print(cnt)