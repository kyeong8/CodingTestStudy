# 대기업 코테 품
# 숫자고르기 골드5
# 딕셔너리 사용
# 꼬리물기 문제 ( 그래프)
# 머리부터 시작해서 다시 머리로 돌아오나 확인
# 순환구조가 아니거나 머리가 아닌 몸통으로 돌아오면 체크 x
n = int(input())
zido = {}
for i in range(1, n + 1):
    zido[i] = int(input())
visited = [0 for _ in range(n + 1)]
result_path = []
for i in range(1, n + 1):
    if visited[i] != 1:
        temp_visited = [0 for _ in range(n + 1)]
        temp_visited[i] = 1
        avail = False
        path = []
        path.append(i)
        num=zido[i]
        while True:
            if temp_visited[num] == 1:
                if num == i:
                    avail = True
                break
            temp_visited[num] = 1
            path.append(num)
            num = zido[num]


        if avail:
            for p in path:
                visited[p]=1
                result_path.append(p)
print(len(result_path))
result_path.sort()
for t in result_path:
    print(t)

