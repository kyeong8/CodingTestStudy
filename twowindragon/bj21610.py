'''
 - 50분 소요
 - 구름 이동, 물 복사, 구름 생성 기능 구현 
 - 구름 이동할 때, 격자를 벗어나면 격자 크기만큼 나눠줌
 - water_dict -> 물 복사량 저장 {(x, y): 대각 방향 물이 있는 칸의 수}

'''
from collections import defaultdict


def check_outside(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    return True


def change_outside(x, y):
    if x < 0 or x >= N:
        x %= N
    if y < 0 or y >= N:
        y %= N
    return x, y


def move_cloud(d, s):
    new_cloud = []
    for i in range(len(cloud)):
        x, y = cloud[i]
        nx = x + dx[d] * s
        ny = y + dy[d] * s
        nx, ny = change_outside(nx, ny)
        new_cloud.append((nx, ny))
        disappeared_cloud.add((nx, ny))  # 사라진 구름 -> 구름 생성에서 고려
        graph[nx][ny] += 1
    return new_cloud


def duplicate_water():
    water_dict = defaultdict(int)
    ddx = [-1, -1, 1, 1]
    ddy = [-1, 1, -1, 1]
    for i in range(len(cloud)):
        x, y = cloud[i]
        for j in range(4):
            nx = x + ddx[j]
            ny = y + ddy[j]
            if not check_outside(nx, ny):
                continue
            if graph[nx][ny] > 0:
                water_dict[(x, y)] += 1 

    for x, y in water_dict:
        graph[x][y] += water_dict[(x, y)]


def generate_cloud():
    new_cloud = []
    for x in range(N):
        for y in range(N):
            if graph[x][y] >= 2 and (x, y) not in disappeared_cloud:
                new_cloud.append((x, y))
                graph[x][y] -= 2

    return new_cloud


N, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
move_info = []
for _ in range(M):
    d, s = map(int, input().split())
    move_info.append((d - 1, s))

dx = [0, -1, -1, -1, 0, 1, 1, 1]
dy = [-1, -1, 0, 1, 1, 1, 0, -1]
cloud = [(N - 1, 0), (N - 1, 1), (N - 2, 0), (N - 2, 1)]
answer = 0

for i in range(M):
    d, s = move_info[i]
    disappeared_cloud = set()
    cloud = move_cloud(d, s)
    duplicate_water()
    cloud = generate_cloud()

print(sum([graph[x][y] for y in range(N) for x in range(N)]))
