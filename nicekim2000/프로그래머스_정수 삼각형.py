def solution(triangle):
    for i in range(1, len(triangle)):
        for j in range(len(triangle[i])):
            temp = []
            if j - 1 >= 0:
                temp.append(triangle[i - 1][j - 1] + triangle[i][j])
            if j + 1 <= i:
                temp.append(triangle[i - 1][j] + triangle[i][j])
            triangle[i][j] = max(temp)
    return max(triangle[-1])


a = [[7], [3, 8], [8, 1, 0], [2, 7, 4, 4], [4, 5, 2, 6, 5]]
solution(a)
