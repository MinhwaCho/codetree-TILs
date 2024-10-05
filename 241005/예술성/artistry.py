# n = 5
# matrix = [[1,2,2,3,3],[2,2,2,3,3],[2,2,1,3,1],
#           [2,2,1,1,1],[2,2,1,1,1]]
import sys
input = sys.stdin.readline

n = int(input())
matrix = [list(map(int, input().split())) for _ in range(n)]

def dfs(r, c):
    direction = [(-1,0), (1,0), (0,-1), (0,1)]

    visited[r][c] = True
    q = [(r,c)]
    target_num = matrix[r][c]
    _group = [target_num, (r,c)]

    # print(">>>", q, target_num)
    while q:
        # print(q)
        r, c = q.pop()
        for i in range(len(direction)):
            ar, ac = r+direction[i][0], c+direction[i][1]
            if -1<ar<n and -1<ac<n and not visited[ar][ac] and target_num == matrix[ar][ac]:
                visited[ar][ac] = True
                q.append((ar,ac))
                _group.append((ar,ac))
    group.append(_group)
    # print("+++", group)

def search_group():
    global visited
    global group

    for i in range(n):
        for j in range(n):
            if not visited[i][j]:
                dfs(i, j)

def compute_score(ind1, ind2):
    group_1, group_2 = group[ind1][1:], group[ind2][1:]
    direction = [(-1,0), (1,0), (0,-1), (0,1)]
    cnt = 0
    for r, c in group_1:
        for i in range(len(direction)):
            ar, ac = r + direction[i][0], c + direction[i][1]
            if (ar, ac) in group_2:
                cnt += 1
    return (len(group_1) + len(group_2)) * group[ind1][0] * group[ind2][0] * cnt

def cal_score(group):
    # global visited
    # visited = [False]*len(group)
    all_art_score = 0
    
    def dfs_c(ind):
        nonlocal all_art_score
        if sum(visited) == 2:
            target_group_1, target_group_2 = [index for index in range(len(visited)) if visited[index]][0], [index for index in range(len(visited)) if visited[index]][1]
            # print(visited,target_group_1,target_group_2) # compute score
            art_score = compute_score(target_group_1,target_group_2)
            # print(art_score)
            all_art_score += art_score
            return
        else:
            for i in range(ind, len(group)):
                if not visited[i]:
                    visited[i] = True
                    dfs_c(i)
                    visited[i] = False      

    dfs_c(0)
    return all_art_score

# 3-1. 십자모양 회전
def rotate_op_90(mat):
    new_mat = list(reversed(list(zip(*mat))))
    return new_mat

def rotate_90(mat):
    n = len(mat)
    m = len(mat[0])
    new_mat = [[0]*m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            new_mat[j][n-i-1] = mat[i][j]
    return new_mat

def rotate_all():
    rotate_matrix = [[-1]*n for i in range(n)]
    # print(matrix)
    # print([matrix[n//2][:]]+[[row[n//2] for row in matrix]])

    cross_rot_matrix = rotate_op_90(matrix)
    # print(list(cross_rot_matrix[2][:]), [row[n//2] for row in cross_rot_matrix])
    rotate_matrix[n//2][:] = cross_rot_matrix[n//2][:]
    for row in range(len(cross_rot_matrix)):
        rotate_matrix[row][n//2] = cross_rot_matrix[row][n//2]

    def rotate_square(x_start, y_start):
        mat = list()
        for i in range(x_start,x_start+(n//2)):
            new_m = []
            for j in range(y_start,y_start+(n//2)):
                new_m.append(matrix[i][j])
            mat.append(new_m)
        mat = rotate_90(mat)
        
        for i in range(n//2):
            for j in range(n//2):
                rotate_matrix[x_start+i][y_start+j] = mat[i][j]

    rotate_square(0, 0)
    rotate_square(0, (n//2)+1)
    rotate_square((n//2)+1, 0)
    rotate_square((n//2)+1, (n//2)+1)

    return rotate_matrix


result = 0
for i in range(4):
    # print(matrix)
    # 1. Group 나누기
    visited = [[False]*n for _ in range(n)]
    group = list()
    search_group()
    # print(group)

    # 2. 예술점수 구하기
    visited = [False]*len(group)
    art_score = cal_score(group)
    result += art_score
    # print(art_score)

    # 3. 회전
    matrix = rotate_all()

print(result)