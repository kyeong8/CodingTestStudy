# 주사위 굴리기2
# (x, y)에서 동서남북 방향으로 연속해서 이동할 수 있는 칸의 수 C -> 이게 무슨 개소리인거야
# 지도에서 같은 점수를 가진 이어진 칸의 갯수인가 ? 문제에는 설명이 없는데요 ?

# bfs 와 주사위 굴린후 위치 이용
# solve time : 50분 정도?

from collections import deque
def east(dice):
    temp=dice[3][1]
    dice[3][1]=dice[1][2]
    dice[1][2]=dice[1][1]
    dice[1][1]=dice[1][0]
    dice[1][0]=temp
    return dice

def west(dice):
    temp=dice[3][1]
    dice[3][1]=dice[1][0]
    dice[1][0]=dice[1][1]
    dice[1][1]=dice[1][2]
    dice[1][2]=temp
    return dice

def north(dice):
    temp=dice[0][1]
    dice[0][1]=dice[1][1]
    dice[1][1]=dice[2][1]
    dice[2][1]=dice[3][1]
    dice[3][1]=temp
    return dice

def south(dice):
    temp=dice[3][1]
    dice[3][1]=dice[2][1]
    dice[2][1]=dice[1][1]
    dice[1][1]=dice[0][1]
    dice[0][1]=temp
    return dice

def bfs(zido,score_map,r,c):
    path=[(r,c)]
    queue=deque([])
    queue.append((r,c))
    value=zido[r][c]
    count=1
    dr,dc=[0,1,0,-1],[1,0,-1,0]
    score_map[r][c]=n*m+1
    while queue:
        r,c=queue.popleft()
        for i in range(4):
            new_r,new_c=r+dr[i],c+dc[i]
            if new_r < 0 or new_r >= n or new_c < 0 or new_c >= m: continue
            if score_map[new_r][new_c]==n*m+1: continue
            if zido[new_r][new_c]!=value : continue
            score_map[new_r][new_c]=n*m+1
            path.append((new_r,new_c))
            queue.append((new_r,new_c))
            count+=1
    for pr,pc in path:
        score_map[pr][pc]=count
    return score_map

n, m, k = map(int, input().split())
zido = []
for _ in range(n):
    zido.append(list(map(int, input().split())))
dice = [[0, 2, 0],
        [4, 1, 3],
        [0, 5, 0],
        [0, 6, 0]]
# 0123 -> 동남서북
dir=0
r,c=0,0
dr,dc=[0,1,0,-1],[1,0,-1,0]
score_map=[[0 for _ in range(m)] for _ in range(n)]
score=0
for i in range(k):
    # 주사위 방향대로 한 칸 움직이기
    new_r,new_c=r+dr[dir],c+dc[dir]
    # 맵 밖이라면 반대방향 진행
    if new_r < 0 or new_r >= n or new_c < 0 or new_c >=m:
        dir=(dir+2)%4
        new_r, new_c = r + dr[dir], c + dc[dir]

    # B값 계산
    B=zido[new_r][new_c]

    # C값 계산 지도를 통해 각 칸이 몇 점인지 계산
    if score_map[new_r][new_c]==0 :
        score_map=bfs(zido,score_map,new_r,new_c)
    C=score_map[new_r][new_c]

    # 총 점수 계산 후 합산
    score+=B*C

    # 주사위 전개도 업데이트
    if dir==0:
        dice=east(dice)
    elif dir==1:
        dice=south(dice)
    elif dir==2:
        dice=west(dice)
    else :
        dice=north(dice)

    # 업데이트 후 주사위의 다음 이동 방향 정하기
    A=dice[3][1]
    if A>B:
        dir = (dir + 1) % 4
    elif A<B:
        dir = (dir - 1) % 4

    r,c=new_r,new_c
print(score)