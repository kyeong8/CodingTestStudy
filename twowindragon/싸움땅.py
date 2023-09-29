'''
 - 한시간 반, 쉬운 편
 - 함수화를 많이 해보려고 노력
 - 총 교체, 플레이어 이동, 이동 후 칸에 플레이어 있는지 확인, 결투, 결투 후 승자와, 패자 행동 구현
 - 총을 dict로 -> 같은 칸에 여러 총이 있을 수 있으니 -> {(x, y) : [1, 3]}
 - player는 리스트에 저장 -> 순서대로 행동을 해야 하기 때문에
 - 총을 교체할 때는 해당 칸에 총이 있는지 확인 -> 있으면 max 값 뽑고, 내가 소지한 총보다 크면 교체, 내가 소지한 총이 0일땐 내려놓지 않음
'''

from collections import defaultdict


def check_outside(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return True
    return False


def move_player(x, y, d):
    nx = x + dx[d]
    ny = y + dy[d]
    if check_outside(nx, ny):
        d = (d + 2) % 4
        nx = x + dx[d]
        ny = y + dy[d]
    return nx, ny, d


def change_gun(idx):
    x, y, d, s, g = players[idx]
    if (x, y) not in gun_dict:
        return
    if not gun_dict[(x, y)]:
        return
    max_gun = max(gun_dict[(x, y)])
    if max_gun > g:
        players[idx] = (x, y, d, s, max_gun)
        gun_dict[(x, y)].remove(max_gun)
        if g != 0:
            gun_dict[(x, y)].append(g)
    return


def check_player(x, y, s):
    for i in range(M):
        nx, ny, _, ns, _ = players[i]
        if nx == x and ny == y and ns != s:
            return i
    return -1


def fight(idx, idx2):
    x, y, d, s, g = players[idx]
    x2, y2, d2, s2, g2 = players[idx2]
    player1_power = s + g
    player2_power = s2 + g2
    point = abs(player1_power - player2_power)
    if player1_power > player2_power:
        answer[idx] += point
        return idx, idx2
    elif player1_power < player2_power:
        answer[idx2] += point
        return idx2, idx
    else:
        if s > s2:
            return idx, idx2
        else:
            return idx2, idx


def loser_action(idx):
    x, y, d, s, g = players[idx]
    players[idx] = (x, y, d, s, 0)
    if g != 0:
        gun_dict[(x, y)].append(g)
    for i in range(4):
        nd = (d + i) % 4
        nx = x + dx[nd]
        ny = y + dy[nd]
        if check_outside(nx, ny):
            continue
        if check_player(nx, ny, s) == -1:
            players[idx] = (nx, ny, nd, s, 0)
            change_gun(idx)
            break
    return


def winner_action(idx):
    change_gun(idx)


N, M, K = map(int, input().split())
guns = []
gun_dict = defaultdict(list)
players = []
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
answer = [0] * M

for i in range(N):
    guns.append(list(map(int, input().split())))
    for j in range(N):
        if guns[i][j] > 0:
            gun_dict[(i, j)].append((guns[i][j]))

for _ in range(M):
    x, y, d, s = map(int, input().split())
    players.append((x - 1, y - 1, d, s, 0))

for _ in range(K):
    for idx in range(M):
        x, y, d, s, g = players[idx]
        x, y, d = move_player(x, y, d)
        players[idx] = (x, y, d, s, g)
        idx2 = check_player(x, y, s)
        if idx2 == -1:
            change_gun(idx)
        else:
            winner_idx, loser_idx = fight(idx, idx2)
            loser_action(loser_idx)
            winner_action(winner_idx)

print(*answer)