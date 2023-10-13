'''
 - 1시간 48분 소요
 - 초기에 번호 순서대로 좌표를 리스트에 저장 [(3, 2), (4, 2) ..... (0, 0)] : N * N - 1 개
   -> 좌표 순서 탐색이 쉬워짐
 - 구현해야하는 기능: 마법 사용, 구슬 이동, 구슬 폭발, 구슬 그룹화

'''


def save_path():
    dx = [0, 1, 0, -1]
    dy = [-1, 0, 1, 0]
    x, y = N // 2, N // 2  # 시작 좌표
    d, dist, move_count = 0, 1, 0  # 방향, 동일한 방향대로 이동해야 하는 거리, 같은 거리만큼 움직인 횟수
    while True:
        for _ in range(dist):
            nx = x + dx[d]
            ny = y + dy[d]
            if nx == 0 and ny == -1:  # 끝
                return
            path.append((nx, ny))
            x, y = nx, ny

        d = (d + 1) % 4  # 방향 변경
        move_count += 1
        if move_count == 2:  # 같은 거리만큼 두 번 움직이면 이동해야 하는 거리를 하나 늘림
            move_count = 0
            dist += 1


def cast_magic(d, s):
    x, y = N // 2, N // 2
    for i in range(1, s + 1):
        nx = x + dx[d] * i
        ny = y + dy[d] * i
        if graph[nx][ny] == 0:
            break
        graph[nx][ny] = 0


def move_guseul():
    new_graph = [[0] * N for _ in range(N)]
    new_guseul = []
    for x, y in path:
        if graph[x][y] == 0:  # 0을 제외한 구슬들을 저장
            continue
        new_guseul.append((graph[x][y]))

    for i in range(len(new_guseul)):  # 새로운 그래프에 0을 제외한 구슬들 저장
        x, y = path[i]
        new_graph[x][y] = new_guseul[i]
    return new_graph


def explode_guseul():
    explosion = False  # 폭발 확인
    cnt = 1  # 같은 구슬의 수
    x, y = path[0]
    if graph[x][y] == 0:  # 처음부터 0인 경우 -> 폭발 안일어남
        return explosion
    last_idx = len(path)
    temp = graph[x][y]
    for i in range(1, len(path)):
        x, y = path[i]
        if graph[x][y] == 0:  # 0인 구슬이 나오면 종료 -> path는 항상 모든 경로를 포함하기 때문에
            last_idx = i
            break
        if temp == graph[x][y]:
            cnt += 1
        else:  # 기준 구슬과 다른 구슬이 나오면
            if cnt >= 4:  # 같은 구슬이 4개 이상일 때
                explosion = True # 폭발이 일어남
                for nx, ny in path[i - cnt: i]:
                    graph[nx][ny] = 0
                answer[temp - 1] += cnt
            cnt = 1
            temp = graph[x][y]

    if cnt >= 4: # 마지막 폭발에 대해서 고려
        for nx, ny in path[last_idx - cnt: last_idx]:
            graph[nx][ny] = 0
        answer[temp - 1] += cnt
        explosion = True
    return explosion


def group_guseul():
    new_graph = [[0] * N for _ in range(N)]
    new_guseul = []
    cnt = 1
    x, y = path[0]
    if graph[x][y] == 0:
        return new_graph # 얘 때문에 type error 났었음

    temp = graph[x][y]
    for i in range(1, len(path)):
        x, y = path[i]
        if graph[x][y] == 0:
            break

        if temp == graph[x][y]: # 같은 구슬의 개수 
            cnt += 1
        else: # 다른 구슬이 나오면, [개수, 번호] 형태로 저장
            new_guseul.extend([cnt, temp])
            cnt = 1
            temp = graph[x][y]
            
    new_guseul.extend([cnt, temp]) # 마지막 그룹 고려

    for i in range(len(new_guseul[:len(path)])): # 기존의 경로 보다 크면 무시
        x, y = path[i]
        new_graph[x][y] = new_guseul[i]
    return new_graph


N, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
magic, path = [], []
for _ in range(M):
    d, s = map(int, input().split())
    magic.append((d - 1, s))  # 마법 (방향, 거리) 저장

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
answer = [0, 0, 0]  # 터뜨린 구슬의 개수 저장

save_path()  # 경로 저장

for i in range(M):
    d, s = magic[i]
    cast_magic(d, s)  # 마법 사용
    graph = move_guseul()  # 구슬 이동
    while explode_guseul():  # 폭발할 구슬이 없을 때까지 폭발, 이동 반복
        graph = move_guseul()
    graph = group_guseul()  # 구슬 그룹화

print(sum([answer[i - 1] * i for i in range(1, 4)]))
