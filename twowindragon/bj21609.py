'''
 - 1시간 20분 소요
 - 270도 회전, 중력(밑으로 칸 내리기), 블록제거, 그룹 찾기 
 - 그룹의 조건: 일반 1개 이상, 검은 색 X, 무지개 상관 ㄴ -> 인접한 블럭, 2개 이상, 일반은 색 동일
    -> 기준 블록 조건: 무지개 x, 행 작, 열 작
 - 그룹 찾을 때 visited와 inner_visited 두 개 사용
    -> visited는 기준 블록들의 방문 체크, 즉 무지개는 체크 안함
    -> inner_visited는 bfs 내부에서 방문했던 곳을 가지 않기 위해 사용
- pos2group는 {(x,y) 기준 블록의 좌표: [(x2, y2)......(xn, yn)] 그룹내 좌표들}
  -> 조건에 맞는 그룹 찾은 후, 해당 그룹을 삭제할 때 사용
  
 - 밑으로 땡기는 코드가 중요한 듯 -> 2048의 땡기는 코드와 동일
'''

from collections import deque
from collections import defaultdict


def search_group():
    group = []
    for x in range(N):
        for y in range(N):
            if graph[x][y] > 0 and not visited[x][y]:
                visited[x][y] = True
                temp = BFS(x, y) # temp 는 그룹의 정보 [전체 칸 수, 무지개 수, x, y]
                if temp[0] >= 2: # 전체 칸 수가 2개 이상이면
                    group.append(temp) # 그룹 리스트에 저장
    return group


def BFS(s_x, s_y):
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]
    inner_visited = [[False] * N for _ in range(N)] # 무지개 칸
    q = deque([(s_x, s_y)])
    inner_visited[s_x][s_y] = True
    v = graph[s_x][s_y]
    whole_cnt, rainbow_cnt = 1, 0

    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx >= N or ny < 0 or ny >= N:
                continue
            if (graph[nx][ny] == 0 or graph[nx][ny] == v) and not inner_visited[nx][ny]:
                q.append((nx, ny))
                pos2group[(s_x, s_y)].append((nx, ny))
                inner_visited[nx][ny] = True
                whole_cnt += 1
                if graph[nx][ny] == v:
                    visited[nx][ny] = True
                else:
                    rainbow_cnt += 1
    return [whole_cnt, rainbow_cnt, s_x, s_y]


def remove_block(x, y):
    graph[x][y] = -2
    for i, j in pos2group[(x, y)]:
        graph[i][j] = -2


def rotate_270(g):
    temp_graph = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            temp_graph[N - 1 - j][i] = g[i][j]

    return temp_graph


def gravity():
    for j in range(N):
        pointer = N - 1
        for i in range(N - 2, -1, -1):
            if graph[i][j] == -1:
                pointer = i
                continue
            if graph[i][j] >= 0:
                temp = graph[i][j]
                graph[i][j] = -2
                if graph[pointer][j] == -2:
                    graph[pointer][j] = temp
                    pointer -= 1
                else:
                    pointer -= 1
                    graph[pointer][j] = temp


N, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
answer = 0

while True:
    visited = [[False] * N for _ in range(N)]
    pos2group = defaultdict(list)
    group = search_group()
    if not group:
        break
    cnt, _, x, y = sorted(group)[-1] # 가장 크고, 무지개가 많고, 행 크고, 열이 큰 그룹
    remove_block(x, y)
    answer += cnt ** 2
    gravity() # 중력
    graph = rotate_270(graph) # 회전
    gravity() # 중력

print(answer)
