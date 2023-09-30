'''
 - 2시간 10분 소요
 - pos2team -> {좌표: 팀번호}, team2pos -> {팀번호: deque[(x, y) ....)]}
 - 저장하는 과정이 복잡했 -> dfs로 찾는게 나을듯
   -> 머리를 기준으로 4방향을 탐색, 1다음 바로 3을 찾는 경우 제외
   -> 팀원이 있던 좌표는 모두 4로 변경
 -
'''
from collections import defaultdict
from collections import deque


def save_team():
    cnt = 1
    for i in range(N):
        for j in range(N):

            if graph[i][j] == 1:
                x, y = i, j
                pos2team[(x, y)] = cnt
                team2pos[cnt].append((x, y))
                graph[x][y] = 4
                while True:
                    for d in range(4):
                        nx = x + dx[d]
                        ny = y + dy[d]
                        if not check_outside(nx, ny):
                            continue

                        if graph[nx][ny] == 3 and len(team2pos[cnt]) < 2:
                            continue
                        if 1 < graph[nx][ny] < 4 and (nx, ny) not in pos2team:
                            x, y = nx, ny
                            pos2team[(x, y)] = cnt
                            team2pos[cnt].append((x, y))
                            if graph[x][y] == 2:
                                graph[x][y] = 4
                            break

                    if graph[x][y] == 3:
                        graph[x][y] = 4
                        cnt += 1
                        break


def team_move():
    for n in range(M):
        h_x, h_y = team2pos[n + 1][0]
        e_x, e_y = team2pos[n + 1][-1]
        for i in range(4):
            nx = h_x + dx[i]
            ny = h_y + dy[i]
            if not check_outside(nx, ny):
                continue
            if graph[nx][ny] == 4:
                if (nx, ny) in pos2team and (e_x != nx or e_y != ny):
                    continue

                team2pos[n + 1].appendleft((nx, ny))
                del_x, del_y = team2pos[n + 1].pop()
                del pos2team[(del_x, del_y)]
                pos2team[(nx, ny)] = n + 1
                break


def check_outside(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    return True


def shoot(i):
    a = i // N % 4
    b = i % N
    score, k = 0, 0

    if a == 0:
        for y in range(N):
            if (b, y) in pos2team:
                num = pos2team[(b, y)]
                k = team2pos[num].index((b, y)) + 1
                team2pos[num].reverse()
                break

    elif a == 1:
        for x in range(N - 1, -1, -1):
            if (x, b) in pos2team:
                num = pos2team[(x, b)]
                k = team2pos[num].index((x, b)) + 1
                team2pos[num].reverse()
                break

    elif a == 2:
        for y in range(N - 1, -1, -1):
            if (N - 1 - b, y) in pos2team:
                num = pos2team[(N - 1 - b, y)]
                k = team2pos[num].index((N - 1 - b, y)) + 1
                team2pos[num].reverse()
                break
    else:
        for x in range(N):
            if (x, N - 1 - b) in pos2team:
                num = pos2team[(x, N - 1 - b)]
                k = team2pos[num].index((x, N - 1 - b)) + 1
                team2pos[num].reverse()
                break

    score = k ** 2
    return score


N, M, K = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]
pos2team = {}
team2pos = defaultdict(deque)
answer = 0

save_team()
for i in range(K):
    team_move()
    answer += shoot(i)

print(answer)