# 2023-09-21
# bj23290_마법사 상어와 복제
# 3시간
# 깡 구현함
# 구현, 시뮬레이션
# 깡구현

# 물고기가 방향에 따라 이동하는 함수
def fish_move(fishes, smell, shark):
    dx = [0, -1, -1, -1, 0, 1, 1, 1]
    dy = [-1, -1, 0, 1, 1, 1, 0, -1]
    new_fishes = []
    for f in fishes:
        fx, fy, d = f
        orignal_d = d
        # 갈 수 있는 방향을 찾을 때까지 반복
        try_count = 0
        while True:
            if try_count == 8:
                d -= 1
                new_dir = (d - 1) % 8
                new_fishes.append([fx, fy, orignal_d])
                break
            try_count += 1
            new_dir = (d - 1) % 8
            new_fx = fx + dx[new_dir]
            new_fy = fy + dy[new_dir]
            # 게임장 밖인 경우
            if new_fx > 4 or new_fx <= 0 or new_fy > 4 or new_fy <= 0:
                d -= 1
                continue
            # 냄새가 남아있는 경우
            if [new_fx, new_fy] in [s[:2] for s in smell]:
                d -= 1
                continue
            # 상어님이 있는 경우
            if [new_fx, new_fy] == shark:
                d -= 1
                continue
            # 무사히 통과하면 이동 후 리스트에 삽입
            new_fishes.append([new_fx, new_fy, (new_dir + 1)])
            break
    return new_fishes


# 상어의 공격 차례
def shark_turn(shark, new_fishes):
    # 0제외 길이가 16인 배열에 물고기 갯수 저장
    # x*y로 좌표 변환
    fish_info = [0 for _ in range(17)]
    for f in new_fishes:
        fish_info[4 * (f[0] - 1) + f[1]] += 1
    smell = []
    # 상어 이동 DFS 발동
    shark_info = shark_move(shark, fish_info, 0, 0, 0, smell)
    sharks = []
    for i in shark_info:
        for j in i:
            for k in j:
                sharks.append(k)
    # 우선 순위대로 정렬
    sorted_shark = sorted(sharks, key=lambda x: (-x[0], x[1]))
    # 상어 이동
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]
    fisrt, second, third = sorted_shark[0][1] // 100, sorted_shark[0][1] % 100 // 10, sorted_shark[0][1] % 10
    shark[0] = shark[0] + dx[fisrt - 1] + dx[second - 1] + dx[third - 1]
    shark[1] = shark[1] + dy[fisrt - 1] + dy[second - 1] + dy[third - 1]
    # 물고기 삭제 과정
    return_fishes = []
    for f in new_fishes:
        if [f[0], f[1], 3] in sorted_shark[0][2]:
            continue
        return_fishes.append(f)
    return [shark, return_fishes, sorted_shark[0][2]]


# 상어 이동 DFS - 종료 조건 : 움직일 때마다 count 해서 3번 움직이면 종료
# 인자 : 상어좌표,각 칸에 물고기 갯수,상어가 움직인 힛수, 상어가 움직일 때 값(나중에 사전순 정렬용),상어가 잡아먹은 물고기 수 , 물고기 비린내 좌표
def shark_move(shark, fish_info, moving_count, move_value, fish_count, smell):
    shark_info = []
    if moving_count == 3:
        result = smell[:]
        return [fish_count, move_value, result]
    dx = [-1, 0, 1, 0]
    dy = [0, -1, 0, 1]
    sx, sy = shark
    for i in range(4):
        fish_eat = False
        temp = 0
        new_sx = sx + dx[i]
        new_sy = sy + dy[i]
        # 맵 이탈 사건
        if new_sx > 4 or new_sx <= 0 or new_sy > 4 or new_sy <= 0:
            continue
        if fish_info[4 * (new_sx - 1) + new_sy] != 0:  # 가는 칸에 물고기가 있는 경우
            # 물고기 죽음처리, 잡아먹은 물고기 수 증가 , 비린내 좌표 추가
            fish_eat = True
            temp = fish_info[4 * (new_sx - 1) + new_sy]
            fish_count += fish_info[4 * (new_sx - 1) + new_sy]
            fish_info[4 * (new_sx - 1) + new_sy] = 0
            smell.append([new_sx, new_sy, 3])
        new_move_value = move_value * 10 + (i + 1)
        shark_info.append(shark_move([new_sx, new_sy], fish_info, moving_count + 1, new_move_value, fish_count, smell))
        # 다시 돌아와서 원래대로 복귀 후 다른 경로 탐색
        if fish_eat:
            fish_count -= temp
            fish_info[4 * (new_sx - 1) + new_sy] = temp
            smell.remove([new_sx, new_sy, 3])
    return shark_info


def smell_down(smell):
    new_smell = []
    for s in smell:
        if s[2] == 2: continue
        s[2] -= 1
        new_smell.append(s)
    return new_smell


m, s = map(int, input().split())
fishes = []
for _ in range(m):
    fish = list(map(int, input().split()))
    fishes.append(fish)
shark = list(map(int, input().split()))
smell = []
for _ in range(s):
    new_fishes = fish_move(fishes, smell, shark)
    # print(new_fishes)
    shark, new_fishes, new_smell = shark_turn(shark, new_fishes)
    smell = smell_down(smell)
    smell += new_smell
    fishes += new_fishes
    # print(smell)
print(len(fishes))
# print(fishes)
# print()
