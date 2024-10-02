import sys
input = sys.stdin.readline
N = int(input())
check_list = [int(input()) for i in range(N)]

target_ind = 0
for i in range(N-1):
    if check_list[i] > check_list[i+1]:
        if i != 0:
            if check_list[i+1] <= check_list[i-1]:
                target_ind = i+1
                arr = check_list[:target_ind]
                
            else:
                target_ind = i
                arr = check_list[target_ind+1:]

# print("target index: ", target_ind)
# print("target num:", check_list[target_ind])
# print("Array:", arr)

cnt = 0
target_num = check_list[target_ind]
if target_ind < N-1 and target_num > check_list[target_ind+1]:
    for i in range(len(arr)):
        if arr[i] < target_num:
            if i < len(arr)-1 and arr[i] == arr[i+1]: continue
            cnt += 1
else:
    for i in range(len(arr)-1,-1,-1):
        if arr[i] > target_num:
            if i >= 1 and arr[i] == arr[i-1]: 
                continue
            else:
                cnt += 1
print(cnt)