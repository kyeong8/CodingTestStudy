'''
 - 1시간 고민 2시간 40분 구현
 - 물고기, 물고기 냄새를 어떻게 저장할지 고민을 길게 함, 이차원행렬, 리스트, 딕셔너리
   -> 기존에 존재하던 물고기(복제되는 물고기)는 리스트에 저장 (x, y, d)
   -> 이동한 물고기, 물고기 냄새는 딕셔너리에 저장 why? del, in 연산자의 복잡도가 빨라서
   -> 같은 칸에 도착하는 물고기가 많을 수 있다 -> defaultdict(list)사용, 키는 좌표, 값은 방향 ex) {(1, 1): [2, 3]}
   -> 물고기 냄새도 키는 좌표, 값은 사라지기 전 남은 시간 저장

 - ***상어랑 물고기는 같은 칸에 존재할 수 있음, 상어는 지나갔던 곳을 또 갈 수 있음 ex) 상 하 상 -> 방문 확인할 필요 없음
 - 물고기 이동은 상어랑 냄새 아닌 곳으로 이동
 - 상어이동은 가장 많이 먹는 방법 -> dfs사용 , 여러개면 사전 순 -> 그냥 이동방향 좌표를 상 좌 하 우 순서대로 저장해놓으면 됨



from collections import defaultdict


def dfs(n, x, y, cnt, shark_path):
'''
    global max_count, max_shark_path
    if n == 3:
        if cnt > max_count:
            max_count = cnt
            max_shark_path = shark_path.copy() # 물고기 가장 많이 먹는 경로 저장
        return
    for i in range(4):
        nx = x + s_dx[i]
        ny = y + s_dy[i]
        if 0 <= nx < 4 and 0 <= ny < 4:
            if (nx, ny) in move_fish: #이동한 곳에 물고기가 있을때
                # 지난 곳을 또 갈 수 있으니까 temp에 저장해놓고 삭제, dfs 돌리고 다시 복구
                temp = move_fish[(nx, ny)]
                del move_fish[(nx, ny)]
                dfs(n + 1, nx, ny, cnt + len(temp), shark_path + [(nx, ny)]) # len(temp)는 이동한 좌표에 있는 물고기 수 
                move_fish[(nx, ny)] = temp
            else:
                dfs(n + 1, nx, ny, cnt, shark_path + [(nx, ny)])

# 입력 받기
M, S = map(int, input().split())
fish = []
for _ in range(M):
    fx, fy, d = map(int, input().split())
    fish.append((fx - 1, fy - 1, d - 1))

sx, sy = map(int, input().split())
sx, sy = sx - 1, sy - 1
# 물고기, 상어 이동
f_dx = [0, -1, -1, -1, 0, 1, 1, 1]
f_dy = [-1, -1, 0, 1, 1, 1, 0, -1]
s_dx = [-1, 0, 1, 0]
s_dy = [0, -1, 0, 1]


fish_smell = {}
for _ in range(S):
    move_fish = defaultdict(list)
    max_count = -1
    max_shark_path = []

    for fx, fy, d in fish:
        not_move = True
        nd = d
        for _ in range(8):
            f_nx = fx + f_dx[d]
            f_ny = fy + f_dy[d]
            if 0 <= f_nx < 4 and 0 <= f_ny < 4 and (f_nx, f_ny) not in fish_smell and (f_nx != sx or f_ny != sy):
                move_fish[(f_nx, f_ny)].append(d)
                not_move = False
                break
            else:
                d = (d - 1) % 8 # 반시계 45도
                continue

        if not_move: # 8방향 다 확인했는데 움직일 수 없으면 가만히 있기
            move_fish[(fx, fy)].append(nd)

    dfs(0, sx, sy, 0, []) # 상어의 경로 찾기
    sx, sy = max_shark_path[2] # 3개의 좌표중 마지막 좌표가 현재 상어의 좌표

    # 상어가 지났던 경로에 있는 물고기들 삭제, 물고기 냄새 저장
    for x, y in max_shark_path: 
        if (x, y) in move_fish:
            del move_fish[(x, y)]
            fish_smell[(x, y)] = 3 # 3으로 저장한 이유는 바로 밑에서 1을 빼주고 바로 확인하기 때문에?

    # 물고기 냄새 -1초
    for x, y in list(fish_smell.keys()):
        fish_smell[(x, y)] -= 1
        if fish_smell[(x, y)] == 0:
            del fish_smell[(x, y)]
            
    # 복제 물고기 + 이동 후 살아남은 물고기
    for x, y in move_fish:
        for d in move_fish[(x, y)]:
            fish.append((x, y, d))

print(len(fish))

