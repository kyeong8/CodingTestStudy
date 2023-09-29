'''
 - 실패
 - 도착지에서 bfs로 모든 격자를 탐색해서 거리는 저장
 - 베이스 캠프 이동 시엔  dist 배열에서 가장 가까운 베이스 캠프(graph[x][y] = 1)인 경우 탐색
 - 가게 이동 시엔 4방향중 dist 값이 가장 작은 값으로 이동
'''

from collections import deque


def BFS(x, y):
    q = deque([(x, y)])
    visited = [[10000] * N for _ in range(N)]
    visited[x][y] = 0
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if 0 <= nx < N and 0 <= ny < N:
                if graph[nx][ny] != -1  and visited[nx][ny] == 10000:
                    visited[nx][ny] = visited[x][y] + 1
                    q.append(((nx, ny)))
    return visited


def go_base(idx):
    if is_arrived(idx):
        return
    min_dist = 1000
    min_x = 0
    min_y = 0
    x, y, = store[idx]
    dist = BFS(x, y)
    # 모든 격자 탐색하면서 베이스캠프인 경우일때 거리 비교를 통해 가장 가까운 베이스 캠프 탐색
    for i in range(N):
        for j in range(N):
            if graph[i][j] != 1:
                continue
            if dist[i][j] < min_dist:
                min_dist = dist[i][j]
                min_x = i
                min_y = j
    people[idx] = (min_x, min_y)
    graph[min_x][min_y] = -1


def go_store(idx):
    if is_arrived(idx):
        return
    min_dist = 1000
    min_dir = -1
    x, y  = store[idx]
    dist = BFS(x, y)
    x, y = people[idx]
    # 4 방향 중 어느 방향이 목적지로부터 가까운지 확인
    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if 0 <= nx < N and 0 <= ny < N:
            if dist[nx][ny] < min_dist:
                min_dist = dist[nx][ny]
                min_dir = i
    people[idx] = (x + dx[min_dir], y + dy[min_dir])


def is_finished():
    for i in range(len(people)):
        if not is_arrived(i):
            return False
    return True


def is_arrived(idx):
    return people[idx] == store[idx]


def check_arrive(idx):
    if is_arrived(idx):
        x, y = people[idx]
        graph[x][y] = -1


N, M = map(int, input().split())
graph =[list(map(int, input().split())) for _ in range(N)]
people = []
store = []
for _ in range(M):
    x, y = map(int, input().split())
    people.append((-1, -1))
    store.append((x - 1, y - 1))

ban = [[False] * N for _ in range(N)]
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

time = 0
while not is_finished():
    time += 1
    for i in range(M):
        if i + 1 < time:
            go_store(i)

    for i in range(M):
        if i + 1 < time:
            check_arrive(i)

    if time <= M:
        go_base(time - 1)
    print(people)


print(time)

