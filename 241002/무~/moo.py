def find_nth_character(N):
    def length_of_s(k):
        # S(k)의 길이를 계산
        if k == 0:
            return 3  # S(0) = "moo"의 길이
        return 2 * length_of_s(k - 1) + (k + 3)

    def solve(k, n):
        if k == 0:
            # S(0) = "moo"
            if n == 1:
                return 'm'
            else:
                return 'o'
        
        left_len = length_of_s(k - 1)  # S(k-1)의 길이
        middle_len = k + 3  # 가운데 "moo...o" 부분의 길이
        
        if n <= left_len:
            # 왼쪽 S(k-1) 부분에 속할 때
            return solve(k - 1, n)
        elif n <= left_len + middle_len:
            # 가운데 "m o o...o" 부분에 속할 때
            if n == left_len + 1:
                return 'm'
            else:
                return 'o'
        else:
            # 오른쪽 S(k-1) 부분에 속할 때
            return solve(k - 1, n - left_len - middle_len)

    # k는 N번째 문자가 존재하는 S(t)에서 t를 찾아야 함
    k = 0
    while length_of_s(k) < N:
        k += 1
    
    return solve(k, N)

# 입력받은 N번째 문자 출력
N = int(input())
print(find_nth_character(N))