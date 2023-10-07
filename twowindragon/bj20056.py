'''
 - 43분 소요
'''
from  collections import defaultdict


def change_outside(x, y):
    if x < 0 or x >= N:
        x %= N
    if y < 0 or y >= N:
        y %= N
    return x, y


def move_fireball(fireballs):
    new_fireball = defaultdict(list)
    for x, y in fireballs:
        for fireball in fireballs[(x, y)]:
            m, s, d = fireball
            nx = x + dx[d] * s
            ny = y + dy[d] * s
            nx, ny = change_outside(nx, ny)
            new_fireball[(nx, ny)].append((m, s, d))
    return new_fireball


def divide_fireball(fireballs):
    for x, y in list(fireballs.keys()):
        n = len(fireballs[(x, y)])
        if n < 2:
            continue
        sum_m, sum_s = 0, 0
        flag_d = True
        prev_d = 1 if fireballs[(x, y)][0][2] & 1 else 0
        for fireball in fireballs[(x, y)]:
            m, s, d = fireball
            sum_m += m
            sum_s += s
            current_d = 1 if d & 1 else 0
            if prev_d != current_d:
                flag_d = False
            else:
                prev_d = current_d
        new_m = sum_m // 5
        new_s = sum_s // n

        if new_m != 0:
            if flag_d:
                fireballs[(x, y)] = [(new_m, new_s, i) for i in range(0, 7, 2)]
            else:
                fireballs[(x, y)] = [(new_m, new_s, i) for i in range(1, 8, 2)]
        else:
            del fireballs[(x, y)]

    return fireballs


def score():
    answer = 0
    for x, y in pos2fireball:
        for m, s, d in pos2fireball[(x, y)]:
            answer += m
    return answer


N, M, K = map(int, input().split())
pos2fireball = defaultdict(list)

dx = [-1, -1, 0, 1, 1, 1, 0, -1]
dy = [0, 1, 1, 1, 0, -1, -1, -1]

for _ in range(M):
    x, y, m, s, d = map(int, input().split())
    pos2fireball[(x - 1, y - 1)].append((m, s, d))

for _ in range(K):
    pos2fireball = move_fireball(pos2fireball)
    pos2fireball = divide_fireball(pos2fireball)

print(score())