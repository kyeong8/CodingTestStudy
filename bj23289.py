'''
 - 1시간 고민 1시간 49분 구현
 - 온풍기는 리스트에 저장, 벽은 (x, y, t)로 set에 저장 -> 순서가 필요 없기 때문에
 - 온풍기 바람은 재귀적으로 구현 , 세 곳으로 퍼지도록 함 -> visit을 사용해서 이미 바람이 지났는지 확인
   -> 온풍기 방향에 따라 따로 따로 구현
 - 온도조절은 동시에 이동 -> 이동량을 따로 새로운 그래프에 저장해놓고 기존의 그래프에 더해줌
   -> 오른쪽와 아래쪽만 탐색
   -> 어항정리의 물고기 이동이랑 완전 동일

 - ***바깥쪽 빼줄때 중복되는 부분을 빼줘서 찾는데 오래걸림
 
'''
def heater_on(n, x, y, t):
    if n == 0:
        return
    if n == 5:
        nx, ny = x + dx[t - 1], y + dy[t - 1]
        graph[nx][ny] += n
        heater_on(n - 1, nx, ny, t)
        return

    if t == 1:  # 온풍기가 오른쪽
        if 0 <= x + 1 < R and 0 <= y + 1 < C and not visited[x + 1][y + 1]:
            if (x + 1, y, 0) not in wall and (x + 1, y, 1) not in wall:
                visited[x + 1][y + 1] = True
                graph[x + 1][y + 1] += n
                heater_on(n - 1, x + 1, y + 1, t)

        if 0 <= x < R and 0 <= y + 1 < C and  not visited[x][y + 1]:
            if (x, y, 1) not in wall:
                visited[x][y + 1] = True
                graph[x][y + 1] += n
                heater_on(n - 1, x, y + 1, t)

        if 0 <= x - 1 < R and 0 <= y + 1 < C and not visited[x - 1][y + 1]:
            if (x, y, 0) not in wall and (x - 1, y, 1) not in wall:
                visited[x - 1][y + 1] = True
                graph[x - 1][y + 1] += n
                heater_on(n - 1, x - 1, y + 1, t)
                
    elif t == 2: # 온풍기가 왼쪽 
        if 0 <= x - 1 < R and 0 <= y - 1 < C and not visited[x - 1][y - 1]:
            if (x, y, 0) not in wall and (x - 1, y - 1, 1) not in wall:
                visited[x - 1][y - 1] = True
                graph[x - 1][y - 1] += n
                heater_on(n - 1, x - 1, y - 1, t)

        if 0 <= x < R and 0 <= y - 1 < C and  not visited[x][y - 1]:
            if (x, y - 1, 1) not in wall:
                visited[x][y - 1] = True
                graph[x][y - 1] += n
                heater_on(n - 1, x, y - 1, t)

        if 0 <= x + 1 < R and 0 <= y - 1 < C and not visited[x + 1][y - 1]:
            if (x + 1, y, 0) not in wall and (x + 1, y - 1, 1) not in wall:
                visited[x + 1][y - 1] = True
                graph[x + 1][y - 1] += n
                heater_on(n - 1, x + 1, y - 1, t)

    elif t == 3: # 온풍기가 위쪽
        if 0 <= x - 1 < R and 0 <= y - 1 < C and not visited[x - 1][y - 1]:
            if (x, y - 1, 0) not in wall and (x, y - 1, 1) not in wall:
                visited[x - 1][y - 1] = True
                graph[x - 1][y - 1] += n
                heater_on(n - 1, x - 1, y - 1, t)

        if 0 <= x - 1 < R and 0 <= y < C and not visited[x - 1][y]:
            if (x, y, 0) not in wall:
                visited[x - 1][y] = True
                graph[x - 1][y] += n
                heater_on(n - 1, x - 1, y, t)

        if 0 <= x - 1 < R and 0 <= y + 1 < C and not visited[x - 1][y + 1]:
            if (x, y + 1, 0) not in wall and (x, y, 1) not in wall:
                visited[x - 1][y + 1] = True
                graph[x - 1][y + 1] += n
                heater_on(n - 1, x - 1, y + 1, t)

    else: # 온풍기가 아래쪽
        if 0 <= x + 1 < R and 0 <= y - 1 < C and not visited[x + 1][y - 1]:
            if (x + 1, y - 1, 0) not in wall and (x, y - 1, 1) not in wall:
                visited[x + 1][y - 1] = True
                graph[x + 1][y - 1] += n
                heater_on(n - 1, x + 1, y - 1, t)

        if 0 <= x + 1 < R and 0 <= y < C and not visited[x + 1][y]:
            if (x + 1, y, 0) not in wall:
                visited[x + 1][y] = True
                graph[x + 1][y] += n
                heater_on(n - 1, x + 1, y, t)

        if 0 <= x + 1 < R and 0 <= y + 1 < C and not visited[x + 1][y + 1]:
            if (x + 1, y + 1, 0) not in wall and (x, y, 1) not in wall:
                visited[x + 1][y + 1] = True
                graph[x + 1][y + 1] += n
                heater_on(n - 1, x + 1, y + 1, t)


def tmp_move(graph):
    temp_graph = [[0] * C for _ in range(R)]
    for x in range(R):
        for y in range(C):
            if y + 1 < C and (x, y, 1) not in wall: # 오른쪽으로 이동가능한지 확인
                d = abs(graph[x][y] - graph[x][y + 1]) // 4
                if d > 0:                             
                    if graph[x][y] > graph[x][y + 1]: # 왼쪽이 더 클 때
                        temp_graph[x][y] -= d
                        temp_graph[x][y + 1] += d
                    else:                             # 오른쪽이 더 클 때
                        temp_graph[x][y + 1] -= d
                        temp_graph[x][y] += d

            if x + 1 < R and (x + 1, y, 0) not in wall: # 밑쪽으로 이동가능한지 확인
                d = abs(graph[x][y] - graph[x + 1][y]) // 4
                if d > 0:
                    if graph[x][y] > graph[x + 1][y]: # 위쪽이 더 클 때
                        temp_graph[x][y] -= d
                        temp_graph[x + 1][y] += d
                    else:                             # 아래쪽이 더 클 때
                        temp_graph[x + 1][y] -= d
                        temp_graph[x][y] += d
        for y in range(C):
            graph[x][y] += temp_graph[x][y]

    return graph


def outside_minus():               # 바깥쪽 -1
    for y in range(C):
        if graph[0][y] > 0:
            graph[0][y] -= 1

        if graph[-1][y] > 0:
            graph[-1][y] -= 1
                              
    for x in range(1, R - 1):      # 위에서 빼줬기 때문에 범위를 1 ~ R - 1로 지정
        if graph[x][0] > 0:
            graph[x][0] -= 1

        if graph[x][-1] > 0:
            graph[x][-1] -= 1


R, C, K = map(int, input().split())
heater = []
graph = []
check_space = []  # 조사할 칸
wall = set()
answer = 0
for i in range(R):
    graph.append(list(map(int, input().split())))
    for j in range(C):
        if graph[i][j] == 0:
            continue
        if graph[i][j] == 5:
                check_space.append((i, j))
        else:
            heater.append((i, j, graph[i][j]))
        graph[i][j] = 0


W = int(input())
for _ in range(W):
    x, y, t = map(int, input().split())
    wall.add((x - 1, y - 1, t))
# wall = {(3, 4 ,1), (3, 2, 1), (1, 2, 1), (2, 2, 0)}

dx = [0, 0, -1, 1]
dy = [1, -1, 0, 0]
# wall = {(2, 3, 1), (2, 4, 0)}

for _ in range(100):
    cnt = 0
    for x, y, t in heater:
        visited = [[False] * C for _ in range(R)]
        heater_on(5, x, y, t)

    graph = tmp_move(graph)
    outside_minus()
    answer += 1

    for x, y in check_space:
        if graph[x][y] >= K:
            cnt += 1

    if cnt == len(check_space):
        print(answer)
        exit()

print(101)
