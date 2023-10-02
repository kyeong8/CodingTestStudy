'''
 - 점수 계산, 회전 구현
 - 회전 공식 -> rotate[j - old_j + old_i][k - 1 - (i - old_i) + old_j] = graph[i][j]
   -> old_j, old_i는 부분 정사각형의 맨 왼쪽 위 값 -> 원점으로 몰아주기 위한 작업
 - bfs로 각 그룹을 탐색 -> pos2group({(x, y): group}, group2pos 생성 {group : [(x, y), (x2, y2) ..]}
 - 맞닿은 변의 수는 이차원 배열에 저장, 행과 열은 그룹 넘버를 뜻함
 - pos2group은 맞닿은 변의 수를 구할때 사용
'''
from collections import deque
from collections import defaultdict


def rotate():
    k = (N - 1) // 2
    rotated_graph = [[0] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            if 0 <= i < k and 0 <= j < k:  # 맨 왼쪽 위 구역
                rotated_graph[j][k - 1 - i] = graph[i][j]
            elif 0 <= i < k and k < j:     # 맨 오른쪽 위 구역
                rotated_graph[j - (k + 1)][k - 1 - (i - 0) + k + 1] = graph[i][j]
            elif k < i and 0 <= j < k:     # 왼쪽 아래 구역
                rotated_graph[j + (k + 1)][k - 1 - (i - (k + 1))] = graph[i][j]
            elif k < i and k < j:          # 오른쪽 아래 구역
                rotated_graph[j][k - 1 - (i - (k + 1)) + k + 1] = graph[i][j]
            # 십자가 구역
            elif i == k:                   
                rotated_graph[N - 1 - j][i] = graph[i][j]
            elif j == k:
                rotated_graph[j][i] = graph[i][j]

    return rotated_graph


def check_outside(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    return True


def BFS(x, y, n):
    q = deque([(x, y)])
    v = graph[x][y]
    visited[x][y] = True
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if not check_outside(nx, ny):
                continue
            if not visited[nx][ny] and graph[nx][ny] == v: # 탐색시작한 값과 동일한 경우
                group2pos[n].append((nx, ny))
                pos2group[(nx, ny)] = n
                q.append((nx, ny))
                visited[nx][ny] = True


def calculate_facing(): # 팀별로 맞닿은 변의 수 계산
    for x in range(N):
        for y in range(N):
            group_num = pos2group[(x, y)] # 현재 좌표의 그룹 넘버
            for i in range(2, 4):
                nx = x + dx[i]
                ny = y + dy[i]
                if not check_outside(nx, ny):
                    continue
                group_num2 = pos2group[(nx, ny)] # 맞닿은 좌표의 그룹 넘버
                facing[group_num][group_num2] += 1
                facing[group_num2][group_num] += 1


def calculate_score():
    global answer
    for i in range(len(group2pos)): # 그룹끼리 맞닿은 변이 1개 이상일 경우 점수 계산
        for j in range(i + 1, len(group2pos)):
            facing_num = facing[i][j]
            if facing_num <= 0:
                continue

            a_num = len(group2pos[i]) # 칸의 수
            b_num = len(group2pos[j])
            a_x, a_y = group2pos[i][0] 
            b_x, b_y = group2pos[j][0]
            a_value = graph[a_x][a_y] # 그룹의 값
            b_value = graph[b_x][b_y]
            answer += (a_num + b_num) * a_value * b_value * facing_num

def save_dict(): # pos2group, group2pos dict 생성
    n = 0 # 그룹 넘버
    for i in range(N):
        for j in range(N):
            if not visited[i][j]:
                pos2group[(i, j)] = n 
                group2pos[n].append((i, j))
                BFS(i, j, n)
                n += 1


dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]
N = int(input())
graph = [list(map(int, input().split())) for _ in range(N)]
answer = 0

for i in range(4):
    visited = [[False] * N for _ in range(N)]
    group2pos = defaultdict(list)
    pos2group = {}
    save_dict()
    facing = [[0] * len(group2pos) for _ in range(len(group2pos))]
    calculate_facing()
    calculate_score()
    if i == 4: 
        break
    graph = rotate()

print(answer)