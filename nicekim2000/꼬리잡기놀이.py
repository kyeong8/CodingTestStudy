from collections import deque

# bfs 인데 한 방향찾으면 종료하는 조건
def bfs(zido, n, visited, r, c):
    queue = deque()
    path = [(r, c)]
    queue.append((r, c))
    direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    visited[r][c] = 1
    while queue:
        r, c = queue.pop()
        for dir in direction:
            new_r, new_c = r + dir[0], c + dir[1]
            if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n:
                continue
            if visited[new_r][new_c] == 1 or zido[new_r][new_c] == 0:
                continue
            visited[new_r][new_c] = 1
            path.append((new_r, new_c))
            queue.append((new_r, new_c))
            break
    return visited, path

n, m, k = map(int, input().split())
zido = []
for _ in range(n):
    zido.append(list(map(int, input().split())))

visited = [[0 for _ in range(n)] for _ in range(n)]
count = 0
escape = False
paths = []

# 입력에서 m개의 경로는 찾는다.
# 0이 아닌 값이 있다면 그 점을 기준으로 bfs경로 탐색해서 하나의 경로를 찾음
# m개의 경로를 찾으면 종료
for i in range(n):
    if escape: break
    for j in range(n):
        if zido[i][j] >= 1 and visited[i][j] == 0:
            visited, temp_path = bfs(zido, n, visited, i, j)
            paths.append(temp_path)
            count += 1
        if count == m:
            escape = True
            break
info = []

# 찾은 경로들에서 머리와 꼬리를 구분하고 팀원들의 수, 맨 처음 방향(시계 or 반시계)
# 원래방향(현재 어느 방향으로 진행하는지 알기위해), 경로 전체 길이 등을 하나의 클래스 다루듯이 배열에 저장
for path in paths:
    for i in range(len(path)):
        r, c = path[i][0], path[i][1]
        # 머리 발견
        if zido[r][c] == 1:
            # 시계방향
            if zido[path[(i -1) % len(path)][0]][path[(i -1) % len(path)][1]] == 2:
                temp = (i - 1) % len(path)
                count=2
                while True:
                    # 꼬리발견
                    if zido[path[temp][0]][path[temp][1]] == 3:
                        break
                    temp = (temp - 1) % len(path)
                    count+=1
                # [머리인덱스,꼬리인덱스,방향(1 : 시계 , -1 : 반시계),경로길이,경로,팀원수,원래 방향]
                ttemp = [i, temp, 1, len(path), path,count,-1]
                info.append(ttemp)
                break
            # 반시계 방향
            else:
                temp = (i + 1) % len(path)
                count=2
                while True:
                    # 꼬리발견
                    if zido[path[temp][0]][path[temp][1]] == 3:
                        break
                    temp = (temp + 1) % len(path)
                    count+=1
                # [머리인덱스,꼬리인덱스,방향(1 : 시계 , -1 : 반시계),경로길이,경로]
                ttemp = [i, temp, -1, len(path), path,count,1]
                info.append(ttemp)
                break

#공 던지기를 대비하여 k번째 반복할 때 공의 시작위치와 진행방향을 계산했다.
stage_dir=[(1,0),(0,1),(-1,0),(0,-1)]
round_dir=[(0,1),(-1,0),(0,-1),(1,0)]
point_pos=[0,0]
point=0
for i in range(k):
    # 라운드에 따른 공 포지션 세팅
    ball_meet=False
    number = [[0 for _ in range(n)] for _ in range(n)]
    value=i%(4*n)
    stage=value//n
    num=value%n
    if num!=0 :
        point_pos = [point_pos[0] + stage_dir[stage][0], point_pos[1] + stage_dir[stage][1]]

    # 각 머리와 꼬리의 인덱스를 한 칸씩 이동
    for j in range(len(info)):
        team=info[j]
        # 한 칸씩 인덱스 이동
        team[0]=(team[0]+team[2])%team[3]
        team[1]=(team[1]+team[2])%team[3]x

        count=1
        start=team[0]
        # 뱀들의 번호를 새로운 지도에다 저장 머리부터 1,2,3,4,5
        for _ in range(team[5]):
            number[team[4][start][0]][team[4][start][1]]=count
            start=(start+team[6])%team[3]
            count+=1

        # print()
    # 공을 던지기 시작
    # 정해준 위치부터 한 칸식 이동해서 처음 뱀을 만날때 까지
    for a in range(n):
        new_r,new_c=point_pos[0]+a*round_dir[stage][0],point_pos[1]+a*round_dir[stage][1]
        # 뱀을 만났을 때
        if number[new_r][new_c]!=0:
            team=[]
            # 어느 팀인지 조사
            for i in range(len(paths)):
                if (new_r,new_c) in paths[i]:
                    team=info[i]
                    break
            # 해당 팀의 진행방향을 바꾸고 포인트 정산
            if team[6]!=team[2]*-1:
                point=point+(team[5]+1-number[new_r][new_c])*(team[5]+1-number[new_r][new_c])
            else : point=point+number[new_r][new_c]*number[new_r][new_c]
            team[2]*=-1
            ball_meet=True
            break

print(point)



