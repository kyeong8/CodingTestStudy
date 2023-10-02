'''
 - 쉬운 편에 속함
 - 나무 성장, 나무 번식, 제초제 위치 선정, 제초제 뿌리기, 제초제 삭제 구현
 - 제초제만 dict에 저장 {(x,y): 유효기간}, 나머지는 이차원 배열에 표현
 - 나무성장, 번식은 동시에 이루어짐, 새로운 그래프 생성 필요
 - 나무 성장은 오른쪽, 아래 방향만 탐색하면 됨
 - 나무 번식은 네방향 확인 하면서 빈칸이고, 제초제가 없을 경우를 리스트에 저장
 - 제초제 위치 선정도 완탐 -> 가장 많이 죽일 수 있는 x, y, 수 리턴
 - ********ㄴ제초제 뿌릴때 나무가 없는 칸을 만나면, 그 칸 까지는 제초제를 뿌림
'''

def check_outside(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    return True


def grow_tree():
    temp_graph = [[0] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            if graph[x][y] <= 0:
                continue
            if check_outside(x + 1, y): # 아래 탐색
                if graph[x + 1][y] > 0:
                    temp_graph[x][y] += 1
                    temp_graph[x + 1][y] += 1

            if check_outside(x, y + 1): # 오른쪽 탐색
                if graph[x][y + 1] > 0:
                    temp_graph[x][y] += 1
                    temp_graph[x][y + 1] += 1

        for y in range(N): # 기존의 그래프에 더해주기
            graph[x][y] += temp_graph[x][y]


def breed_tree():
    temp_graph = [[0] * N for _ in range(N)]
    for x in range(N):
        for y in range(N):
            blank = []
            if graph[x][y] <= 0: # 나무가 없을 경우 
                continue
            for i in range(4): # 4방향 탐색
                nx = x + dx[i]
                ny = y + dy[i]
                if check_outside(nx, ny) and graph[nx][ny] == 0 and (nx, ny) not in drug: # 빈칸이고, 제초제가 없을 경우
                    blank.append((nx, ny)) 

            if not blank: # 나무 주위에 번식 가능한 경우가 없을때
                continue

            breed = graph[x][y] // len(blank)
            for xx, yy in blank: # 번식
                temp_graph[xx][yy] += breed

    for x in range(N):   # 기존의 그래프에 번식한 나무 더하기
        for y in range(N):
            graph[x][y] += temp_graph[x][y]


def drug_position():
    max_die = 0
    max_x, max_y = -1, -1
    for x in range(N):
        for y in range(N):
            if graph[x][y] <= 0:
                continue
            die = graph[x][y]
            for i in range(4, 8):
                nx, ny = x + dx[i], y + dy[i]
                k = 1
                while check_outside(nx, ny) and graph[nx][ny] > 0:
                    die += graph[nx][ny]
                    if k >= K:
                        break
                    nx += dx[i]
                    ny += dy[i]
                    k += 1

            if die > max_die:
                max_die = die
                max_x = x
                max_y = y

    return max_x, max_y, max_die


def drug_attack(x, y):
    graph[x][y] = 0
    drug[(x, y)] = C + 1
    for i in range(4, 8):
        nx, ny = x + dx[i], y + dy[i]
        k = 1
        while check_outside(nx, ny) and graph[nx][ny] >= 0:
            drug[(nx, ny)] = C + 1
            if graph[nx][ny] == 0:
                break
            graph[nx][ny] = 0
            if k >= K:
                break
            nx += dx[i]
            ny += dy[i]
            k += 1

def drug_clean(): # 1씩 줄여주면서 0이 되면 제초제 삭제
    for x, y in list(drug.keys()):
        drug[(x, y)] -= 1
        if drug[(x, y)] == 0:
            del drug[(x, y)]


N, M, K, C = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(N)]
dx = [-1, 0, 1, 0, -1, -1, 1, 1]
dy = [0, -1, 0, 1, -1, 1, -1, 1]
answer = 0
drug = {}


for i in range(M):
    grow_tree()
    breed_tree()
    x, y, die = drug_position()
    answer += die
    drug_attack(x, y)
    drug_clean()


print(answer)