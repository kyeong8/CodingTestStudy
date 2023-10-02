# 우선 순위 상좌우하

# 분마다 반복
# 맨 처음에는 최단 루트를 구한다 (우선순위를 지켜가며)
# 최단 루트는 자신의 길에 편의점이 있었는데 해당 편의점이 누구에게 정복 당하거나 사람이 들어간 베이스캠프를 지나가는 루트라면 새로운 최단 루트를 구한다.
# 베이스 캠프는 상 , 좌
# 경로기억 bfs와 딕셔너리 사용 !
from collections import deque


def bfs(pos, zido, base,conv, n,opt):
    visited = [[0 for _ in range(n)] for _ in range(n)]
    visited[pos[0]][pos[1]] = 1
    queue = deque([(pos, 0)])  # pos,distance
    direction = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    prev = {pos: None}

    while queue:
        (r, c), d = queue.popleft()
        if (r, c) in base and opt==0:
            path = []
            while (r, c) != pos:
                path.append((r, c))
                r, c = prev[(r, c)]
            path.append((pos))
            return d, list(reversed(path))
        if (r,c) == conv and opt==1:
            path = []
            while (r, c) != pos:
                path.append((r, c))
                r, c = prev[(r, c)]
            path.append((pos))
            return d, list(reversed(path))
        for dr, dc in direction:
            nr, nc = r + dr, c + dc
            if nr < 0 or nr >= n or nc < 0 or nc >= n: continue
            if zido[nr][nc] == -1: continue
            if visited[nr][nc] == 1: continue
            visited[nr][nc] = 1
            prev[(nr, nc)] = (r, c)
            queue.append(((nr, nc), d + 1))
        # 경로 없을 시
    return -1, []


n, m = map(int, input().split())
zido = []
info = {}
for _ in range(n):
    zido.append(list(map(int, input().split())))
conv = []
for _ in range(m):
    conv.append(tuple(map(int, input().split())))
base = []
for i in range(n):
    for j in range(n):
        if zido[i][j] == 1:
            base.append((i, j))
ban = []
minute = 1
# 1분에는 3번과정으로 바로 간다. 베이스 캠프 선택
pos = (conv[0][0] - 1, conv[0][1] - 1)
dist, path = bfs(pos, zido, base,(0,0), n,0)
# print(path)
pr, pc = path.pop()
zido[pr][pc] = -1
ban.append((pr, pc))
info[minute] = [(pr, pc), path]

# print(info)
while True:
    minute += 1
    # 1단계
    # if minute==4:
    #     print()
    ban_set = set(ban)
    new_ban = []
    for key in list(info.keys()):
        temp_path = info[key][1]
        # 길이 막혔다면 새로운 경로를 찾아준다.
        if len(ban_set.intersection((set(temp_path)))) >= 1:
            # print(temp_path)
            dist, path = bfs((info[key][0][0],info[key][0][1]), zido,base,(temp_path[1][0],temp_path[1][1]), n,1)
            # print(path)
            info[key][1] = path[:]
        # 한칸 이동
        # 만약 도착시 새로운 금지 리스트에 등록(임시)
        info[key][0] = info[key][1].pop()
        if len(info[key][1]) == 0:
            zido[info[key][0][0]][info[key][0][1]]=-1
            new_ban.append((info[key][0]))
            del info[key]
    # 아직 출발할 사람이 남았다면
    if minute <= len(conv):
        pos = (conv[minute - 1][0] - 1, conv[minute - 1][1] - 1)
        dist, path = bfs(pos, zido, base,(0,0), n,0)
        pr, pc = path.pop()
        new_ban.append((pr, pc))
        info[minute] = [(pr, pc), path]
    for b in new_ban:
        br,bc=b
        zido[br][bc]=-1
    ban+=new_ban
    # for i in range(n):
    #     print(zido[i])
    # print(ban)
    # print(info)
    # print()
    if len(info) == 0: break
print(minute)
