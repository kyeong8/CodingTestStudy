# 킬러의 이동 좌표와 그 좌표에서 바라보는 방향을 미리 구한다. -> 이거 구현하는데 조금 오래걸림
# 매턴 사람 움직인 다음, 해당 턴에 킬러 좌표와 방향을 구해 사정거리 계산
# 사정 거리 안에 사람이 있고 그 좌표에 나무가 없으면 죽음
n, m, h, k = map(int, input().split())
people = []
trees = []
for _ in range(m):
    temp = list(map(int, input().split()))
    temp[0] -= 1
    temp[1] -= 1
    temp.append(1)  # 1: 정 방향, 0: 반대 방향
    temp.append(1)  # 죽었는지
    people.append(temp)
for _ in range(h):
    tree = list(map(int, input().split()))
    trees.append((tree[0] - 1, tree[1] - 1))
# print(people)
people_move_direction = [[(), (0, -1), (-1, 0)], [(), (0, 1), (1, 0)]]
move_value, move_dir, turn_value = 0, 0, 0
killer = [n // 2, n // 2, 0]
killer_move_direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
reverse_killer_move_direction = [(-1, 0), (0, 1), (1, 0), (0, -1)]
end = False
First = True
track = []
reverse = []
score = 0
for i in range(k):
    # (1,1) 에 도달 하여 반대로 돌아가는 로직
    if end:
        killer = [killer[0] + reverse_killer_move_direction[move_dir][0],
                  killer[1] + reverse_killer_move_direction[move_dir][1],
                  move_dir]
        move_value += 1
        if n - (turn_value // 2 + 1) == move_value:
            if not First:
                turn_value += 1
            move_value = 0
            move_dir = (move_dir - 1) % 4
            killer[2] = move_dir
            First = False
        if killer[0] == n // 2 and killer[1] == n // 2:
            killer[2] = 0
            move_dir, move_value, turn_value = 0, 0, 0
            end = False
    # 중앙에서 달팽이모양으로 가는 로직
    else:
        killer = [killer[0] + killer_move_direction[move_dir][0], killer[1] + killer_move_direction[move_dir][1],
                  move_dir]
        move_value += 1

        if (turn_value // 2) + 1 == move_value:
            turn_value += 1
            move_value = 0
            move_dir = (move_dir + 1) % 4
            killer[2] = move_dir
        if killer[0] == 0 and killer[1] == 0:
            killer[2] = 2
            move_value, turn_value, move_dir = 0, 0, 2
            First = True
            end = True
    track.append(killer)

killer = [n // 2, n // 2, 0]
kill_score=0
for i in range(k):
    # 모든 사람이 죽었다면 끝낸다.
    if kill_score==m : break
    # 사람 이동 차례
    for person in people:
        if person[4] == 0: continue
        if abs(killer[0] - person[0]) + abs(killer[1] - person[1]) >= 4: continue
        pr, pc = person[0], person[1]
        new_r = pr + people_move_direction[person[3]][person[2]][0]
        new_c = pc + people_move_direction[person[3]][person[2]][1]
        # 격자 벗어나는 경우
        if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n:
            # 반대 방향이라고 선언한 후 새로운 좌표 대입
            person[3] = 0 if person[3] == 1 else 1
            new_r = pr + people_move_direction[person[3]][person[2]][0]
            new_c = pc + people_move_direction[person[3]][person[2]][1]
        # 킬러 만나는 칸인 경우 그 자리 얼음
        if [new_r, new_c] == killer[:2]: continue
        # 이동 시 좌표 변환
        person[0], person[1] = new_r, new_c

    # 킬러 차례

    # 킬러의 현재 좌표와 바라보는 방향을 구해서 사정거리를 구한다.
    killer = track[i]
    kr, kc, kd = killer
    # 사정거리 리스트
    kill_path = [(kr, kc)]
    count = 1
    while True:
        new_r, new_c = kr + (count * killer_move_direction[kd][0]), kc + (count * killer_move_direction[kd][1])
        if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n:
            break
        else:
            kill_path.append((new_r, new_c))
            count += 1
        if count == 3: break
    # 현재 턴의 점수
    point = i + 1
    # 잡은 사람회수 변수
    count = 0

    # print(people)
    # print(kill_path)
    # 사람들이 킬러의 사정거리 안에 있는지 검사
    for person in people:
        if person[4] == 0: continue
        if (person[0], person[1]) in kill_path:
            # 나무가 있는 좌표인지 검사
            if (person[0], person[1]) in trees:
                continue
            # 나무가 없다면 죽음 처리
            else:
                kill_score+=1
                count += 1
                person[4] = 0
    score += point * count
print(score)
