'''
 - 41분 소요
 - 토네이도 알고리즘만 알면 됨, 모래 이동은 그냥 노가다 구현

'''


def check_outside(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    return True


def move_sand(x, y, d):
    global answer
    send = graph[x + dx[d]][y + dy[d]]
    graph[x + dx[d]][y + dy[d]] = 0
    oneper = int(send * 0.01)
    twoper = int(send * 0.02)
    fiveper = int(send * 0.05)
    sevenper = int(send * 0.07)
    tenper = int(send * 0.1)
    alphaper = send - oneper * 2 - twoper * 2 - fiveper - sevenper * 2 - tenper * 2

    if d == 0:
        if check_outside(x + 1, y):
            graph[x + 1][y] += oneper
        else:
            answer += oneper
        if check_outside(x - 1, y):
            graph[x - 1][y] += oneper
        else:
            answer += oneper

        if check_outside(x + 1, y - 1):
            graph[x + 1][y - 1] += sevenper
        else:
            answer += sevenper
        if check_outside(x - 1, y - 1):
            graph[x - 1][y - 1] += sevenper
        else:
            answer += sevenper

        if check_outside(x + 2, y - 1):
            graph[x + 2][y - 1] += twoper
        else:
            answer += twoper
        if check_outside(x - 2, y - 1):
            graph[x - 2][y - 1] += twoper
        else:
            answer += twoper

        if check_outside(x + 1, y - 2):
            graph[x + 1][y - 2] += tenper
        else:
            answer += tenper
        if check_outside(x - 1, y - 2):
            graph[x - 1][y - 2] += tenper
        else:
            answer += tenper

        if check_outside(x, y - 3):
            graph[x][y - 3] += fiveper
        else:
            answer += fiveper

        if check_outside(x, y - 2):
            graph[x][y - 2] += alphaper
        else:
            answer += alphaper

    elif d == 1:
        if check_outside(x, y - 1):
            graph[x][y - 1] += oneper
        else:
            answer += oneper
        if check_outside(x, y + 1):
            graph[x][y + 1] += oneper
        else:
            answer += oneper

        if check_outside(x + 1, y + 1):
            graph[x + 1][y + 1] += sevenper
        else:
            answer += sevenper
        if check_outside(x + 1, y - 1):
            graph[x + 1][y - 1] += sevenper
        else:
            answer += sevenper

        if check_outside(x + 1, y - 2):
            graph[x + 1][y - 2] += twoper
        else:
            answer += twoper
        if check_outside(x + 1, y + 2):
            graph[x + 1][y + 2] += twoper
        else:
            answer += twoper

        if check_outside(x + 2, y - 1):
            graph[x + 2][y - 1] += tenper
        else:
            answer += tenper
        if check_outside(x + 2, y + 1):
            graph[x + 2][y + 1] += tenper
        else:
            answer += tenper

        if check_outside(x + 3, y):
            graph[x + 3][y] += fiveper
        else:
            answer += fiveper

        if check_outside(x + 2, y):
            graph[x + 2][y] += alphaper
        else:
            answer += alphaper

    elif d == 2:
        if check_outside(x + 1, y):
            graph[x + 1][y] += oneper
        else:
            answer += oneper
        if check_outside(x - 1, y):
            graph[x - 1][y] += oneper
        else:
            answer += oneper

        if check_outside(x + 1, y + 1):
            graph[x + 1][y + 1] += sevenper
        else:
            answer += sevenper
        if check_outside(x - 1, y + 1):
            graph[x - 1][y + 1] += sevenper
        else:
            answer += sevenper

        if check_outside(x + 2, y + 1):
            graph[x + 2][y + 1] += twoper
        else:
            answer += twoper
        if check_outside(x - 2, y + 1):
            graph[x - 2][y + 1] += twoper
        else:
            answer += twoper

        if check_outside(x + 1, y + 2):
            graph[x + 1][y + 2] += tenper
        else:
            answer += tenper
        if check_outside(x - 1, y + 2):
            graph[x - 1][y + 2] += tenper
        else:
            answer += tenper

        if check_outside(x, y + 3):
            graph[x][y + 3] += fiveper
        else:
            answer += fiveper

        if check_outside(x, y + 2):
            graph[x][y + 2] += alphaper
        else:
            answer += alphaper

    else:
        if check_outside(x, y - 1):
            graph[x][y - 1] += oneper
        else:
            answer += oneper
        if check_outside(x, y + 1):
            graph[x][y + 1] += oneper
        else:
            answer += oneper

        if check_outside(x - 1, y + 1):
            graph[x - 1][y + 1] += sevenper
        else:
            answer += sevenper
        if check_outside(x - 1, y - 1):
            graph[x - 1][y - 1] += sevenper
        else:
            answer += sevenper

        if check_outside(x - 1, y - 2):
            graph[x - 1][y - 2] += twoper
        else:
            answer += twoper
        if check_outside(x - 1, y + 2):
            graph[x - 1][y + 2] += twoper
        else:
            answer += twoper

        if check_outside(x - 2, y - 1):
            graph[x - 2][y - 1] += tenper
        else:
            answer += tenper
        if check_outside(x - 2, y + 1):
            graph[x - 2][y + 1] += tenper
        else:
            answer += tenper

        if check_outside(x - 3, y):
            graph[x - 3][y] += fiveper
        else:
            answer += fiveper

        if check_outside(x - 2, y):
            graph[x - 2][y] += alphaper
        else:
            answer += alphaper


def tornado():
    move_count, direction, dist = 0, 0, 1
    x, y = N // 2, N // 2
    cnt = 1
    while True:
        for i in range(dist):
            nx = x + dx[direction]
            ny = y + dy[direction]
            if nx == 0 and ny == -1:
                return
            if graph[nx][ny] > 0:
                move_sand(x, y, direction)
            graph[nx][ny] = cnt
            cnt += 1
            x, y = nx, ny
        direction = (direction + 1) % 4
        move_count += 1
        if move_count == 2:
            dist += 1
            move_count = 0


N = int(input())
graph = [list(map(int, input().split())) for _ in range(N)]
answer = 0
dx = [0, 1, 0, -1]
dy = [-1, 0, 1, 0]


tornado()
print(answer)

