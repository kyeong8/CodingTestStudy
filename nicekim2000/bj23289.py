from collections import deque

# 오 : 1 왼 : 2 위 : 3 아래 : 4
# 바라보는 쪽의 왼쪽 대각선 갈 수 있는지 점검
def side1(wall_zido, h_r, h_c, d, r, c):
    check_wall = [[3, 1], [4, 2], [2, 3], [1, 4]]
    dr = [-1, 1, 0, 0]
    dc = [0, 0, -1, 1]
    dr2=[0,0,-1,1]
    dc2=[1,-1,0,0]
    first, second = check_wall[d - 1]
    # 가고자 하는 방향에 벽이 있다면
    if first in wall_zido[h_r][h_c]:
        return False
    new_r = h_r + dr[d - 1]
    new_c = h_c + dc[d - 1]
    if new_r < 1 or new_r > r or new_c < 1 or new_c > c:
        return False
    if second in wall_zido[new_r][new_c]:
        return False
    new_r=new_r+dr2[d-1]
    new_c=new_c+dc2[d-1]
    if new_r < 1 or new_r > r or new_c < 1 or new_c > c:
        return False
    return True


# 바라보는 쪽의 오른쪽 대각석 갈 수 있는지 점검
def side2(wall_zido, h_r, h_c, d, r, c):
    check_wall = [[4, 1], [3, 2], [1, 3], [2, 4]]
    dr = [1, -1, 0, 0]
    dc = [0, 0, 1, -1]
    dr2=[0,0,-1,1]
    dc2=[1,-1,0,0]
    first, second = check_wall[d - 1]
    # 가고자 하는 방향에 벽이 있다면
    if first in wall_zido[h_r][h_c]:
        return False
    new_r = h_r + dr[d - 1]
    new_c = h_c + dc[d - 1]
    if new_r < 1 or new_r > r or new_c < 1 or new_c > c:
        return False
    if second in wall_zido[new_r][new_c]:
        return False
    new_r=new_r+dr2[d-1]
    new_c=new_c+dr2[d-1]
    if new_r < 1 or new_r > r or new_c < 1 or new_c > c:
        return False
    return True


# 바로 옆방향 갈 수 있는지 점검
def side(wall_zido, h_r, h_c, d):
    if d in wall_zido[h_r][h_c]:
        return False
    return True


# 오 : 1 왼 : 2 위 : 3 아래 : 4
def spread(temp, h_r, h_c, d, wall_zido, r, c):
    side1_dr = [-1, 1, -1, 1]
    side1_dc = [1, -1, -1, 1]
    side2_dr = [1, -1, -1, 1]
    side2_dc = [1, -1, 1, -1]
    dr = [0, 0, -1, 1]
    dc = [1, -1, 0, 0]
    queue = deque()
    queue.append([h_r, h_c, 5])
    while queue:
        rr, cc, value = queue.popleft()
        # 아니 왜 이게 범위 밖에가 있지 ? 각 함수에서 범위 밖이면 종료조건을 달았는데 흠 ;;
        # 아 내가 잘못했네 ㅋㅋ
        if rr < 1 or rr > r or cc < 1 or cc > c: continue
        temp[rr][cc] = value

        if value == 1: continue
        if rr + dr[d - 1] >= 1 and rr + dr[d - 1] <= r and cc + dc[d - 1] >= 1 and cc + dc[d - 1] <= c:
            if side(wall_zido, rr, cc, d):
                queue.append([rr + dr[d - 1], cc + dc[d - 1], value - 1])
        if side1(wall_zido, rr, cc, d, r, c):
            queue.append([rr + side1_dr[d - 1], cc + side1_dc[d - 1], value - 1])
        if side2(wall_zido, rr, cc, d, r, c):
            queue.append([rr + side2_dr[d - 1], cc + side2_dc[d - 1], value - 1])
    return temp


def wind_calc(wall_zido, r, c, heater):
    dr = [0, 0, -1, 1]
    dc = [1, -1, 0, 0]
    result = []
    for h in heater:
        h_r, h_c, h_d = h
        temp = [[0 for _ in range(c + 1)] for _ in range(r + 1)]
        temp = spread(temp, h_r + dr[h_d - 1], h_c + dc[h_d - 1], h_d, wall_zido, r, c)
        result.append(temp)

    result_arr = [[0 for _ in range(c + 1)] for _ in range(r + 1)]
    for t in result:
        for i in range(1, r + 1):
            for j in range(1, c + 1):
                result_arr[i][j] += t[i][j]

    return result_arr


# 오 : 1 왼 : 2 위 : 3 아래 : 4
# 모든 칸에 대해서 오른쪽과 아래만 검사해서 온도 조절 수행
def control(r, c, temp_zido, wall_zido):
    plus = [[0 for _ in range(c + 1)] for _ in range(r + 1)]
    for i in range(1, r + 1):
        for j in range(1, c + 1):
            # 오른쪽이 있고 벽이 없는 지 검사
            if j + 1 <= c and 1 not in wall_zido[i][j]:
                diff = oper(temp_zido[i][j + 1], temp_zido[i][j])
                plus[i][j] += diff
                plus[i][j + 1] -= diff
            # 아래가 있고 벽이 없는 지 검사
            if i + 1 <= r and 4 not in wall_zido[i][j]:
                diff = oper(temp_zido[i + 1][j], temp_zido[i][j])
                plus[i][j] += diff
                plus[i + 1][j] -= diff
            # # 테두리 온도 감소
            # if i==1 or i==r or j==1 or j==c :
            #     if temp_zido[i][j]>=1:
            #         plus[i][j]-=1

    return plus


def oper(a, b):
    if (a - b) // 4 < 0 and (a - b) % 4 != 0:
        return (a - b) // 4 + 1
    else:
        return (a - b) // 4


def border(temp_zido, r, c):
    for i in range(1, r + 1):
        for j in range(1, c + 1):
            if i == 1 or i == r or j == 1 or j == c:
                if temp_zido[i][j] >= 1:
                    temp_zido[i][j] -= 1
    return temp_zido


r, c, k = map(int, input().split())
zido = []
for _ in range(r):
    zido.append(list(map(int, input().split())))
w = int(input())
wall = []
for _ in range(w):
    wall.append(list(map(int, input().split())))
survey = []
heater = []
for i in range(r):
    for j in range(c):
        if zido[i][j] == 5:
            survey.append([i + 1, j + 1])
        elif 1 <= zido[i][j] <= 4:
            heater.append([i + 1, j + 1, zido[i][j]])
# 오 : 1 왼 : 2 위 : 3 아래 : 4
wall_zido = [[[] for _ in range(c + 1)] for _ in range(r + 1)]
for wa in wall:
    r1, c1, d = wa
    if d == 0:
        wall_zido[r1][c1].append(3)
        if r1 - 1 >= 0:
            wall_zido[r1 - 1][c1].append(4)
    elif d == 1:
        wall_zido[r1][c1].append(1)
        if c1 + 1 <= c:
            wall_zido[r1][c1 + 1].append(2)

temp_zido = [[0 for _ in range(c + 1)] for _ in range(r + 1)]
plus_zido = wind_calc(wall_zido, r, c, heater)
chocolate = 0
# for i in range(1, r + 1):
#     print(plus_zido[i][1:c + 1])
# print()
# 만족할 때 까지 반복
while True:
    if chocolate >= 101:
        break
    # 온풍기 바람 1회 추가
    for i in range(1, r + 1):
        for j in range(1, c + 1):
            temp_zido[i][j] += plus_zido[i][j]
    # for i in range(1,r+1):
    #     print(temp_zido[i][1:c+1])
    # print()
    # 온도 조절
    control_result = control(r, c, temp_zido, wall_zido)
    for i in range(1, r + 1):
        for j in range(1, c + 1):
            temp_zido[i][j] += control_result[i][j]
    temp_zido = border(temp_zido, r, c)
    # for i in range(1,r+1):
    #     print(temp_zido[i][1:c+1])
    # print()
    # 초콜릿냠냠
    chocolate += 1
    # 탈출 조건 검사
    escape = True
    for sr, sc in survey:
        if temp_zido[sr][sc] < k:
            escape = False
            break
    if escape:
        break
print(chocolate)
