'''
 - 대략 3시간 소요
 - 술래의 이동 구현이 중요
 - 도망자는 dict {(x, y): [dir, dir2...]} -> 같은 칸에 여러명 있을 수 있음
 - 나무는 이동하지 않으니 set에 저장 -> in 연산자로 해당 칸에 있는지 확인만 하면 됨
 - 술래와 거리가 3이하인 경우만 이동 -> 술래의 좌표에 -3, +3을 해서 탐색 -> 49칸? 정도만 살피면 됨
 - move_up -> [0, 1, 2, 4, 6, 9, 12, 16, 20 ...] -> 방향이 바뀌는 차례를 미리 저장
 - move_down -> [0, 4, 8, 12, 15, 18, 20, 22, 23....]
 - 해당 턴의 값이 위의 리스트의 특정값과 동일하면 방향이 바뀌어야하고, 아니면 동일한 것임
 24  9 10 11 12   0 15 14 13 12
 23  8  1  2 13   1 16 23 22 11
 22  7  0  3 14   2 17 24 21 10
 21  6  5  4 15   3 18 19 20  9
 20 19 18 17 16   4  5  6  7  8
'''
from collections import defaultdict


def save_tree_theif():
    for _ in range(M):
        x, y, d = map(int, input().split())
        thief[(x - 1, y - 1)].append(d)
    for _ in range(H):
        x, y = map(int, input().split())
        tree_set.add((x - 1, y - 1))

    i = N - 1
    while i > 0:
        move_down.append(move_down[-1] + i)
        move_down.append(move_down[-1] + i)
        i -= 1

    for i in range(1, 11):
        move_up.append(move_up[-1] + i)
        move_up.append(move_up[-1] + i)


def check_outside(x, y):
    if x < 0 or x >= N or y < 0 or y >= N:
        return False
    return True


def move_thief(police_x, police_y):
    new_thief = defaultdict(list)
    for x in range(max(police_x - 3, 0), min(N, police_x + 4)):
        for y in range(max(police_y - 3, 0), min(N, police_y + 4)):
            if abs(x - police_x) + abs(y - police_y) > 3: # 술래와 거리가 3보다 크면
                continue
            if (x, y) in thief: # 해당 칸에 도둑이 있는 경우
                for dir in thief[(x, y)]: # 모든 도둑에 대해서 이동
                    nx = x + dx[dir]
                    ny = y + dy[dir]
                    if not check_outside(nx, ny): # 격자에 벗어날 때
                        dir = (dir + 2) % 4 # 반대 방향으로 변경
                        nx = x + dx[dir]
                        ny = y + dy[dir]
                    if nx == police_x and ny == police_y: # 이동 칸에 술래가 있으면 이동하지 않음
                        new_thief[(x, y)].append(dir)
                    else:
                        new_thief[(nx, ny)].append(dir) 
                del thief[(x, y)] # 해당 칸 모두 이동후 삭제

    for nx, ny in new_thief: # 기존의 도망자 dict에 이동한 도망자들 추가
        thief[(nx, ny)].extend(new_thief[(nx, ny)])


def move_police(x, y, dir, k):
    nx, ny = x + dx[dir], y + dy[dir] # 이동
    up = not ((k - 1) // (N ** 2 - 1)) & 1 # 0, 0으로 가는 방향인지, 중앙으로 가는 방향인지 확인
    k %= N ** 2 - 1 # 5 * 5 형태면 time % 24

    if nx == 0 and ny == 0:
        return nx, ny, 2
    if nx == N // 2 and ny == N // 2:
        return nx, ny, 0
    if up:
        for i in range(len(move_up)):
            if k - move_up[i] == 0:
                return nx, ny, (dir + 1) % 4
            if k - move_up[i] < 0:
                return nx, ny, dir
    else:
        for i in range(len(move_down)):
            if k - move_down[i] == 0:
                return nx, ny, (dir - 1) % 4
            if k - move_down[i] < 0:
                return nx, ny, dir


def catch_thief(x, y, dir):
    catched_thief = 0
    for i in range(3): # 현재칸, + 1, + 2
        nx = x + dx[dir] * i
        ny = y + dy[dir] * i
        if not check_outside(nx, ny): # 격자 벗어나면
            break
        if (nx, ny) in thief and (nx, ny) not in tree_set: # 도둑이 있고, 나무가 없으면
            catched_thief += len(thief[(nx, ny)])
            del thief[(nx, ny)]
    return catched_thief


N, M, H, K = map(int, input().split())
tree_set = set()
thief = defaultdict(list)
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]
move_up = [0]
move_down = [0, N - 1]


answer = 0
police_x, police_y, dir = N //2, N // 2, 0 # 경찰 위치 초기화
save_tree_theif()

for t in range(K):
    move_thief(police_x, police_y) # 도둑 이동
    police_x, police_y, dir = move_police(police_x, police_y, dir, t + 1) # 경찰 이동
    answer += catch_thief(police_x, police_y, dir) * (t + 1) # 도둑 잡기

print(answer)
