# 마법사 상어와 블리자드

# 1트 -> 63퍼에서 걸림
# 반례 1
# 9 1
# 0 0 0 0 0 0 0 0 0
# 3 2 1 3 1 3 3 3 0
# 1 3 3 3 1 3 3 1 0
# 0 2 2 2 1 2 2 1 0
# 0 1 2 1 0 2 2 1 0
# 0 3 3 1 1 2 2 2 0
# 0 3 3 3 1 1 1 2 0
# 0 1 1 1 3 3 3 2 0
# 0 0 0 0 0 0 0 0 0
# 1 3
# 원인 : 꼬리부분의 연속된 구슬을 처리 안함 ( 구슬이 없으면 탈출처리했는데 이전 누적 구슬을 처리하고 넘어가야함) -> 고쳐도 문제는 맞추지 못함
# 반례 2
# 3 1
# 0 2 2
# 2 0 1
# 2 2 2
# 4 1
# 원인 : 구슬 폭발 후 모두 0일 때 복제시 000000 이 나와야 되는데 100000을 하게 함 코드 설계 오류 -> 해결

# bfs , 딕셔너리 사용
# solve time : 1시간 50분 ( 반례를 찾아서 이 정도 ) 반례 없으면 어떡하지 ㅠ
import copy
def fill_blank():
    global pos_to_bead
    # 참조하는 칸의 번호
    ref=1
    new_pos_to_bead={}
    end=False
    start=0
    for i in range(1,n*n):
        if ref == n * n:
            end = True
            start=i
            break
        # 참조하는 값이 0이라면 0이 아닐 때 까지 참조번호 ++
        if pos_to_bead[num_to_pos[ref]]==0:
            while ref<n*n and  pos_to_bead[num_to_pos[ref]]==0:
                ref+=1
            if ref==n*n :
                end=True
                start = i
                break
        new_pos_to_bead[num_to_pos[i]] = pos_to_bead[num_to_pos[ref]]
        # else:
        #     new_pos_to_bead[num_to_pos[i]]=pos_to_bead[num_to_pos[ref]]
        ref+=1
        if ref == n * n:
            end = True
            start = i
            break

    if end:
        for j in range(start,n*n):
            new_pos_to_bead[num_to_pos[j]]=0

    pos_to_bead=copy.deepcopy(new_pos_to_bead)
    return

def boom():
    global pos_to_bead
    prev=4
    count=1
    path=[]
    score=0
    for i in range(1,n*n):
        value=pos_to_bead[num_to_pos[i]]
        # if value==0 : break
        # 연속되지 않은 구슬 일때
        if prev!=value or value==0:
            # 누적된 구슬들이 4개 이상이라면
            if count>=4:
                score+=prev*count
                # 구슬 터짐 처리
                for num in path:
                    pos_to_bead[num_to_pos[num]]=0
            if value==0 : break
            count=1
            prev=value
            path=[i]
        # 연속되는 구슬 일 때
        else :
            count+=1
            path.append(i)
    return score

def duplication():
    global pos_to_bead
    new_pos_to_bead = {}
    ref=1
    prev = pos_to_bead[num_to_pos[1]]
    count = 1
    for i in range(2, n * n):
        value = pos_to_bead[num_to_pos[i]]
        if value == 0:
            if prev==0 : break
            new_pos_to_bead[num_to_pos[ref]] = count
            ref += 1
            if ref == n * n: break
            new_pos_to_bead[num_to_pos[ref]] = prev
            ref += 1
            break

        # 연속되지 않은 구슬 일때
        if prev != value:
            new_pos_to_bead[num_to_pos[ref]]=count
            ref+=1
            if ref==n*n : break
            new_pos_to_bead[num_to_pos[ref]] = prev
            ref+=1
            if ref == n * n: break
            count = 1
            prev = value
        # 연속되는 구슬 일 때
        else:
            count += 1
    for i in range(ref,n*n):
        new_pos_to_bead[num_to_pos[i]] = 0
    pos_to_bead = copy.deepcopy(new_pos_to_bead)
    return




n, m = map(int, input().split())
zido = []
for _ in range(n):
    zido.append(list(map(int, input().split())))
shark = []
for _ in range(m):
    shark.append(tuple(map(int, input().split())))

# 좌표에 칸의 번호
pos_to_num = {}

# 칸의 번호에 좌표
num_to_pos = {}

# 좌표에 구슬 번호
pos_to_bead = {}

r, c = n // 2, n // 2
# 좌,하,우,상
dr, dc = [0, 1, 0, -1], [-1, 0, 1, 0]
dir = 0

num = 1
move_value = 1
move_count = 0
twice = -1
for i in range(1, n * n):
    # move
    r, c = r + dr[dir], c + dc[dir]
    pos_to_num[(r, c)] = i
    num_to_pos[i] = (r, c)
    pos_to_bead[(r, c)] = zido[r][c]
    move_count += 1
    if move_count == move_value:
        dir = (dir + 1) % 4
        move_count = 0
        if twice == 1:
            move_value += 1
        twice *= -1

# print(pos_to_num)
#
# print(num_to_pos)
sr, sc = n // 2, n // 2
# 상하좌우
dr, dc = [-1, 1, 0, 0], [0, 0, -1, 1]
result=0
for i in range(m):

    # 상어의 구슬 먹방
    di, si = shark[i]
    for j in range(1,si+1):

        new_r,new_c=sr+dr[di-1]*j,sc+dc[di-1]*j
        if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n: break
        # 구슬 먹방하면 0으로 처리
        pos_to_bead[(new_r,new_c)]=0

    # 구슬 빈칸 채우기
    fill_blank()


    # 구슬 폭발 ( 터지는게 있을 때까지)
    while True:
        temp_result=boom()
        if temp_result==0: break
        result+=temp_result

        # print(result)
        fill_blank()
        # print(list(pos_to_bead.values()))

    # 구슬 복제
    duplication()
    # print(list(pos_to_bead.values()))


print(result)

