
# 2023-09-25
# 코드트리_포탑 부수기
# 8시간
# 딕셔너리와 queue를 사용한 bfs 사용
# 구현, 시뮬레이션
# 깡 구현함 !
from collections import deque


# bfs 인데 이동 시 자기의 전 칸을 기억해준다
# 이로써 마지막 경로 도달 시 자신의 경로를 파악 할 수 있다.
def bfs(zido, start, end, n, m):
    visited = [[False for _ in range(m)] for _ in range(n)]
    queue = deque([(start, 0)])  # (position, distance)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # 우, 하, 좌, 상
    prev = {start: None}

    while queue:
        (r, c), dist = queue.popleft()
        if (r, c) == end:
            path = []
            while (r, c) != start:
                path.append((r, c))
                r, c = prev[(r, c)]
            path.append(start)
            return dist, list(reversed(path))
        for dr, dc in directions:
            nr, nc = (r + dr) % n, (c + dc) % m
            if not visited[nr][nc] and zido[nr][nc] > 0:
                visited[nr][nc] = True
                prev[(nr, nc)] = (r, c)
                queue.append(((nr, nc), dist + 1))

    return -1, []


def main(n, m, k, grid):
    zido = [row[:] for row in grid]
    turrets = {}  # {공격력: [(r, c)]}
    history = {}  # {(r, c): 몇번째 턴인지}
    turn = 1

    # 딕셔너리 초기화
    for i in range(n):
        for j in range(m):
            if zido[i][j] >= 1:
                if zido[i][j] not in turrets:
                    turrets[zido[i][j]] = []
                turrets[zido[i][j]].append((i, j))
                history[(i, j)] = 0

    while k > 0:
        k -= 1
        # 공격자 선택
        min_attack_value = min(turrets)
        #같은 공격력인 좌표들을 찾고
        attackers = turrets[min_attack_value]
        # 좌표들에 대해 주어진 조건으로 정렬
        attackers.sort(key=lambda pos: (-history[pos], -(pos[0] + pos[1]), -pos[1]))
        attacker_pos = attackers[0]
        history[attacker_pos] = turn
        # 공격자 공격력 수정
        new_attack_value = zido[attacker_pos[0]][attacker_pos[1]] + n + m
        zido[attacker_pos[0]][attacker_pos[1]]=new_attack_value
        turrets[min_attack_value].remove(attacker_pos)
        # 기존 공격력을 포탑 사전에서 삭제
        if not turrets[min_attack_value]:
            del turrets[min_attack_value]

        # 타겟 설정
        # 공격자 설정과 반대로 정렬 후 선택 진행
        max_attack_value = max(turrets)
        targets = turrets[max_attack_value]
        targets.sort(key=lambda pos: (history[pos], pos[0] + pos[1], pos[1]))
        target_pos = targets[0]

        # 타겟 설정에 영향을 안주기위해 이제야 포탑사전에 등록
        turrets[new_attack_value] = turrets.get(new_attack_value, []) + [attacker_pos]

        # bfs로 레이저 공격이 가능한지 판단
        dist, paths = bfs(zido, attacker_pos, target_pos, n, m)

        half_attack_value = new_attack_value // 2
        if dist != -1:  # 레이저 공격이 가능하다면
            # 지나간 패스에 따라 포탑 공격력 감소
            for path in paths:
                if path == attacker_pos:
                    continue
                elif path == target_pos:
                    zido[path[0]][path[1]] -= new_attack_value
                else:
                    zido[path[0]][path[1]] -= half_attack_value
        else:  # 포탑 공격
            zido[target_pos[0]][target_pos[1]] -= new_attack_value
            paths.append((attacker_pos[0],attacker_pos[1]))
            paths.append((target_pos[0],target_pos[1]))
            near = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
            for dr, dc in near:
                if zido[(target_pos[0] + dr) % n][(target_pos[1] + dc) % m] >= 1:
                    if (((target_pos[0] + dr) % n),((target_pos[1] + dc) % m))==attacker_pos : continue
                    zido[(target_pos[0] + dr) % n][(target_pos[1] + dc) % m] -= half_attack_value
                    paths.append((((target_pos[0] + dr) % n),(target_pos[1] + dc) % m))
        # 포탑 사전 초기화 하고 지도를 보고 다시 정의
        turrets = {}
        for i in range(n):
            for j in range(m):
                if zido[i][j] >= 1:
                    if (i, j) not in paths:
                        new_value = zido[i][j] + 1
                        zido[i][j]+=1
                    else:
                        new_value = zido[i][j]
                    if new_value not in turrets:
                        turrets[new_value] = []
                    turrets[new_value].append((i, j))
        # 포탑이 하나 남았다면 종료
        if len(list(turrets.values()))==1 : return max(turrets)
        # 턴 증가
        turn += 1
    # 다 끝나면 가장 강한 포탑 공격력 반환
    return max(turrets)



grid = []
n, m, k = map(int, input().split())
for _ in range(n):
    grid.append(list(map(int, input().split())))

print(main(n, m, k, grid))
