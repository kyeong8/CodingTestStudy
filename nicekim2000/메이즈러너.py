# 2023-09-23
# 코드트리_메이즈 러너
# 4시간
# 최소힙사용, 구현
# 구현, 시뮬레이션
# 깡 구현함 !

import math
import heapq


zido = []
people = []
free = []
whole_move = 0


# 출구자료랑 x좌표 차이, y좌표 차이를 구해 people 변수안에 저장한다.
# 최소힙을 사용해서 출구랑 사람한명을 포함한 정사각형 찾기에서 출구랑 r좌표랑 가까운 순서로, 그 다음은 c 좌표랑 가까운 순서로 사각형을 만들어 보는 방식을사용

def move(n):
    global people, zido, free, whole_move
    dr = [-1, 1, 0, 0]
    dc = [0, 0, 1, -1]
    new_people = []

    while people:
        r, c, _, _ = heapq.heappop(people)
        move_index = -1
        move_value = abs(free[0] - r) + abs(free[1] - c)
        for i in range(4):
            new_r = r + dr[i]
            new_c = c + dc[i]
            if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n: continue
            if zido[new_r][new_c] != 0: continue
            fr, fc = abs(free[0] - new_r), abs(free[1] - new_c)
            temp_move_value = fr + fc
            if temp_move_value < move_value:
                move_value = temp_move_value
                move_index = i
                whole_move += 1
        if move_value == 0: continue
        if move_index != -1:
            r += dr[move_index]
            c += dc[move_index]
        heapq.heappush(new_people, (r, c, abs(free[0] - r), abs(free[1] - c)))
    people = new_people[:]


def rotate(n):
    global people, free, zido

    min_value = n + 1
    sr, sc = [], []
    # 사람들의 좌표를 이용해서 가장 작은 정사각형의 한 변의 길이를 구한다.
    for p in people:
        r, c, fc, fr = p
        temp_min = max(fc, fr) + 1
        if temp_min < min_value:
            min_value = temp_min
            sr, sc = [r], [c]
        elif temp_min == min_value:
            sr.append(r)
            sc.append(c)

    # 출구를 포함한 정사각형을 탐색한다.
    # 탐색은 정사각형의 시작의 r값이 작은순, c값이 작은순으로 탐색한다.
    # 탐색시 모든 정사각형이 map안에 있는지 확인하고, 최소거리를 가진 사람들을 조사하고 정사각형안에 들어간 사람이 있다면
    # 바로 종료
    escape = False
    tr, tc = -1, -1
    for i in range(min_value - 1, -1, -1):
        if escape: break
        for j in range(min_value - 1, -1, -1):
            tr, tc = free[0] - i, free[1] - j
            if tr < 0 or tr + min_value - 1 >= n or tc < 0 or tc + min_value - 1 >= n: continue
            for check_r, check_c in zip(sr, sc):
                if (tr <= check_r < tr + min_value) and (tc <= check_c < tc + min_value):
                    escape = True
                    break
            if escape: break

    # 정해진 정사각형으로 회전 진행
    # map중에 값이 1 이상이면 내구도 감소
    # 원본에서 값을 본떠 회전하고 다시 원본에 삽입하는 방법
    target = zido[tr:tr + min_value]
    target = [target[i][tc:tc + min_value] for i in range(len(target))]
    rotated = [[0 for _ in range(len(target))] for _ in range(len(target[0]))]
    for i in range(len(target)):
        for j in range(len(target[0])):
            if target[i][j] >= 1:
                rotated[j][len(target) - 1 - i] = target[i][j] - 1
            else:
                rotated[j][len(target) - 1 - i] = target[i][j]
    for i in range(tr, tr + min_value):
        zido[i][tc:tc + min_value] = rotated[i - tr][:]

    # 사람들중에 해당 정사각형에 들어가는지 검사한다.
    # 들어 간다면 원점으로 옴겨서 회전 후 다시 되돌려 회전을 진행
    new_people = []
    for p in people:
        r, c, er, ec = p
        if (tr <= r < tr + min_value) and (tc <= c < tc + min_value):
            temp_r = r - tr
            temp_c = c - tc
            new_r = temp_c + tr
            new_c = min_value - 1 - temp_r + tc
            new_people.append((new_r, new_c, er, ec))
        else:
            new_people.append(p)
    heapq.heapify(new_people)
    people = new_people[:]

    # 출구좌표도 같은 방식으로 회전 진행
    temp_free_r = free[0] - tr
    temp_free_c = free[1] - tc
    free[0] = temp_free_c + tr
    free[1] = min_value - 1 - temp_free_r + tc
    return


n, m, k = map(int, input().split())
for _ in range(n):
    zido.append(list(map(int, input().split())))
temp = []
for _ in range(m):
    pr, pc = map(int, input().split())
    pr -= 1
    pc -= 1
    temp.append([pr, pc])
free = list(map(int, input().split()))
free[0] -= 1
free[1] -= 1
for p in temp:
    pr, pc = p
    fr, fc = abs(free[0] - pr), abs(free[1] - pc)
    heapq.heappush(people, (pr, pc, fr, fc))
for _ in range(k):
    move(n)
    if len(people) == 0: break
    rotate(n)

print(whole_move)
print(free[0] + 1, free[1] + 1)
