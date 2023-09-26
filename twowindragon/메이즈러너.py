'''
    - 3시간 17분
    - 사람은 dict에 저장 {(x, y): 사람 수}
    - 탈출구는 e_x, e_y에 저장
    - 가장 작은 정사각형 찾기는  사람과 비상구의 좌표에서 추출가능 -> 모든 사람에 대해서 정사각형의 길이, 왼쪽끝 x, y  좌표를 리스트에 저장 
      -> 정렬해서 조건에 맞는 정사각형만 사용
    - 새로운 그래프를 생성하고(정사각형 크기만큼) 회전한 값을 저장하고 다시 기존의 그래프에 대입
    - 회전한 정사각형안에 사람이 있으면 동일하게 회전 
'''
from collections import defaultdict


def rotation(n, x, y):
    temp_graph = [[0] * n for _ in range(n)]
    temp_people = {}
    for i in range(x, n + x):
        for j in range(y, n + y):
            if graph[i][j] > 0:
                temp_graph[(j - y)][n - 1 - (i - x)] = graph[i][j] - 1
            if (i, j) in new_people: # 만약 회전 칸에 사람이 있으면 temp_people에 저장
                temp_people[((j - y) + x, n - 1 - (i - x) + y)] = new_people[(i, j)]
                del new_people[(i, j)] # 이동 후 삭제

    for i in range(x, n + x):  # 회전 한 부분 다시 기존의 그래프에 복사
        for j in range(y, y + n):
            graph[i][j] = temp_graph[i - x][j - y]

    for x, y in temp_people: # 이동한 사람들 기존의 사람 dict에 옮기기
        new_people[(x, y)] = temp_people[(x, y)]


N, M, K = map(int, input().split())

people = defaultdict(int)
graph = [list(map(int, input().split())) for _ in range(N)]

for _ in range(M):
    x, y = map(int, input().split())
    people[(x - 1, y - 1)] += 1

e_x, e_y = map(int, input().split())
e_x, e_y = e_x - 1, e_y - 1
dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]
answer = 0

for _ in range(K):
    new_people = defaultdict(int)
    squares = [] # 회전할 정사각형 후보들
    for x, y in list(people.keys()):
        current_dist = abs(e_x - x) + abs(e_y - y) # 현재 거리
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx == e_x and ny == e_y:
                answer += people[(x, y)]  # 출구에 도착하면 사람 수만큼 정답에 더해줌
                break
            if 0 <= nx < N and 0 <= ny < N:
                if graph[nx][ny] == 0:
                    new_dist = abs(e_x - nx) + abs(e_y - ny)  # 이동 후 거리
                    if current_dist > new_dist:  # 기존의 거리보다 짧아지면 new_people에 저장, 기존의 딕셔너리에 저장하면 이동 후 또 이동하는 경우 발생
                        new_people[(nx, ny)] += people[(x, y)]
                        answer += people[(x, y)] # 이동거리 더해줌
                        break
        else:
            new_people[(x, y)] += people[(x, y)] # 거리가 줄지 않으면 가만히 있기

    if not new_people: # 만약 새로 이동한 사람이 없으면, 즉 모두 탈출한 경우 break
        break

    for x, y in new_people: # 각 사람과 출구를 이용해 정사각형 후보들 찾기 -> 사람 수 만큼 정사각형 수가 나오게 됨 
        max_diff = max(abs(e_x - x), abs(e_y - y))
        max_x, max_y = max(e_x, x), max(e_y, y)
        squares.append((max_diff + 1, max(0, max_x - max_diff), max(0, max_y - max_diff)))
        
    squares.sort() 
    n, x, y = squares[0] # 조건에 맞는 정사각형
    rotation(n, x, y) # 회전
    e_x, e_y = e_y - y + x, n - 1 - (e_x - x) + y # 탈출구도 좌표 이동
    people = new_people.copy()

print(answer)
print(e_x + 1, e_y + 1)
