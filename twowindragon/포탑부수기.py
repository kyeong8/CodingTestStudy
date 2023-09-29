'''
 - 포탑은 딕셔너리에 저장 {(x,y): (포탑의 공격력, 최근 공격한 time, x, y)}
 - 공격자와 방어자를 뽑을땐 딕셔너리를 정렬해서 양 끝 포탑을 뽑음
 - 레이저 공격시 visited에 경로들을 저장
'''
from collections import deque


def tower_attack(x, y, damage):
    level_up[x][y] = False # 피해를 본 경우 레벨업 불가
    temp = graph[x][y] - damage // 2
    if temp <= 0: # 타워 터지면 제거
        graph[x][y] = 0
        del tower_dict[(x, y)]
    else: # 안 터지면 tower 정보 갱신
        graph[x][y] = temp
        d, t, x, y = tower_dict[(x, y)]
        tower_dict[(x, y)] = (temp, t, x, y)
    return

def tower_enforce():
    for i in range(N):  # 타워 레벨 업
        for j in range(M):
            if graph[i][j] > 0 and level_up[i][j]:
                graph[i][j] += 1
                d, t, x, y = tower_dict[(i, j)]
                tower_dict[(x, y)] = (d + 1, t, x, y)
    return


# 격자를 넘어서면 반대편 좌표 리턴
def opposite(x, y):
    if x < 0:
        x = N - 1
    elif x >= N:
        x = 0

    if y < 0:
        y = M - 1
    elif y >= M:
        y = 0

    return x, y


def razer(a_x, a_y, d_x, d_y, damage):
    visited = [[0] * M for _ in range(N)]
    q = deque([(a_x, a_y)])

    while q:
        x, y = q.popleft()
        if x == d_x and y == d_y:
            path = []
            while True:
                x, y = visited[x][y]
                if x == a_x and y == a_y:
                    break
                path.append((x, y))

            for x, y in path:
                tower_attack(x, y, damage)
            return True

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            nx, ny = opposite(nx, ny)
            if visited[nx][ny] == 0 and graph[nx][ny] != 0:
                visited[nx][ny] = (x, y) # 방문함수에 이전의 좌표를 저장함으로써 최단 경로를 저장할 수 있음
                q.append((nx, ny))
            elif graph[nx][ny] == 0 and nx == d_x and ny == d_y: # 방어하는 타워가 터진 경우도 존재
                q.append((nx, ny))
                visited[nx][ny] = (x, y)
    return False


def cannon(a_x, a_y, d_x, d_y, damage):
    for i in range(8):
        nx = d_x + dx[i]
        ny = d_y + dy[i]
        nx, ny = opposite(nx, ny)
        if graph[nx][ny] > 0 and (nx != a_x or ny != a_y):
            tower_attack(nx, ny, damage)
    return


N, M, K = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
dx = [0, 1, 0, -1, -1, -1, 1, 1]  # 우하좌상
dy = [1, 0, -1, 0, -1, 1, -1, 1]
tower_dict = {}
for i in range(N):
    for j in range(M):
        if graph[i][j] > 0:
            tower_dict[(i, j)] = (graph[i][j], 0, i, j)

for n in range(K):
    tower = list(tower_dict.values()) # 정렬을 위해 리스트로 변환
    level_up = [[True] * M for _ in range(N)]

    if len(tower) == 1: # 남은 타워 1개면 종료
        break
    tower = sorted(tower, key=lambda x: (x[0], -x[1], -(x[2] + x[3]), -x[3]))
    damage, time, a_x, a_y = tower[0] # 공격자
    defence, time2, d_x, d_y = tower[-1] # 방어자
    graph[a_x][a_y] += N + M
    damage = graph[a_x][a_y]
    tower_dict[(a_x, a_y)] = (damage, n + 1, a_x, a_y) # 타워 갱신 -> n + 1은 현재 공격한 타임
    defence = max(0, graph[d_x][d_y] - graph[a_x][a_y])
    graph[d_x][d_y] = defence

    if defence > 0:
        tower_dict[(d_x, d_y)] = (defence, time2, d_x, d_y)
    else:
        del tower_dict[(d_x, d_y)]

    level_up[a_x][a_y] = False
    level_up[d_x][d_y] = False

    flag = razer(a_x, a_y, d_x, d_y, damage)
    if not flag:
        cannon(a_x, a_y, d_x, d_y, damage)

    tower_enforce()


tower = list(tower_dict.values())
tower.sort(key=lambda x: (x[0], -x[1], -(x[2] + x[3]), -x[3]))
answer = tower[-1][0]
print(answer)