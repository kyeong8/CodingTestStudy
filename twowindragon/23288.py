'''
 - 43분 소요
 - 이동할때 다이스 바뀌는 것만 잘 저장하면 문제없음
 - 기능들을 나눠서 구현하자...
'''
from collections import deque


def change_dice(d): # 다이스가 이동할때 눈 변경
    if d == 0:
        dice[0], dice[1], dice[4], dice[5] = dice[4], dice[0], dice[5], dice[1]
    elif d == 1:
        dice[0], dice[2], dice[3], dice[5] = dice[3], dice[0], dice[5], dice[2]
    elif d == 2:
        dice[0], dice[1], dice[4], dice[5] = dice[1], dice[5], dice[0], dice[4]
    else:
        dice[0], dice[2], dice[3], dice[5] = dice[2], dice[5], dice[0], dice[3]


def check_outside(x, y):
    if x < 0 or x >= N or y < 0 or y >= M:
        return False
    return True


def move_dice(x, y, d): # 주사위 이동 
    nx = x + dx[d]
    ny = y + dy[d]
    if not check_outside(nx, ny): # 격자 벗어나면 반대방향으로
        d = (d + 2) % 4
        nx = x + dx[d]
        ny = y + dy[d]

    return nx, ny, d


def score_dice(x, y): # bfs 사용..
    visited = [[False] * M for _ in range(N)]
    b = graph[x][y]
    q = deque([(x, y)])
    visited[x][y] = True
    cnt = 1
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if not check_outside(nx, ny):
                continue
            if graph[nx][ny] == b and not visited[nx][ny]: # 같은 정수일때만 이동
                cnt += 1
                visited[nx][ny] = True
                q.append((nx, ny))
                
    return cnt * b


def change_direction(x, y, d): # 주사위 아랫 면과 지도에 써진 점수 비교해서 방향 바꾸기
    bottom = dice[5]
    B = graph[x][y]
    if bottom > B:
        d = (d + 1) % 4
    elif bottom < B:
        d = (d - 1) % 4
    return d


N, M, K = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
dice = [1, 2, 3, 4, 5, 6]
answer = 0
direction = 1
dice_x, dice_y = 0, 0

for i in range(K):
    dice_x, dice_y, direction = move_dice(dice_x, dice_y, direction)
    change_dice(direction)
    answer += score_dice(dice_x, dice_y)
    direction = change_direction(dice_x, dice_y, direction)

print(answer)