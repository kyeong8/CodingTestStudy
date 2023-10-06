'''
 - 49분 소요 
 - 회전 코드 또 나옴 (메이즈러너, 예술성) 예술성이랑  완전히 동일
 - 돌리고, 동시에 감소시키기
 - 오른쪽, 아래만 탐색해서 주위 얼음이 있는 칸의 수를 저장
 
'''

from collections import deque


def check_outside(x, y):
    if x < 0 or x >= n or y < 0 or y >= n:
        return False
    return True


def rotation_90(l, graph):  # 돌려돌려
    k = 2 ** l
    new_graph = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            old_x, old_y = x // k * k, y // k * k
            new_graph[y - old_y + old_x][k - 1 - (x - old_x) + old_y] = graph[x][y]

    return new_graph


def melt_ice():  # 녹이기
    blank = [[0] * n for _ in range(n)]
    for x in range(n):
        for y in range(n):
            if graph[x][y] == 0:
                continue
            for i in range(2, 4):
                nx = x + dx[i]
                ny = y + dy[i]
                if not check_outside(nx, ny):
                    continue
                if graph[nx][ny] > 0:
                    blank[x][y] += 1
                    blank[nx][ny] += 1

        for y in range(n):
            if graph[x][y] == 0:
                continue
            if blank[x][y] < 3:  # 주위 얼음이 3개 미만이면 -1 
                graph[x][y] -= 1


def BFS(x, y):
    q = deque([(x, y)])
    visited[x][y] = True
    size = 1
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if not check_outside(nx, ny):
                continue
            if graph[nx][ny] > 0 and not visited[nx][ny]:
                q.append((nx, ny))
                size += 1
                visited[nx][ny] = True
    return size


def find_biggest():  # bfs로 가장 큰 그룹의 사이즈 찾기
    max_size = 0
    for x in range(n):
        for y in range(n):
            if graph[x][y] == 0:
                continue
            if not visited[x][y]:
                max_size = max(max_size, BFS(x, y))
    return max_size


N, Q = map(int, input().split())
n = 2 ** N
graph = [list(map(int, input().split())) for _ in range(n)]
L = list(map(int, input().split()))
visited = [[False] * n for _ in range(n)]

dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

for i in L:
    graph = rotation_90(i, graph)
    melt_ice()

print(sum(map(sum, graph)))
print(find_biggest())
