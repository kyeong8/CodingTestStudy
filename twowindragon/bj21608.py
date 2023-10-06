'''
 - 1시간 반
 - pos2blank {(x, y): 주위의 빈칸수},    student_to_like {학생 번호: [좋아하는 학생 번호들}  -> 점수 계산할 때 한 번 사용
 - student_to_pose {학생 번호: (x, y)} -> 현재 할당해야 하는 학생이 좋아하는 학생이 필드에 있는지 확인하기 위해 사용
 - 현재 할당해야 하는 학생이 좋아하는 학생이 필드에 있으면 -> 좋아하는 학생들의 4방향을 탐색 (이미 할당된 자리 제외)  
                                                  -> 탐색한 자리에서 다시 4방향씩 탐색하면서 각 자리의 (인접한 좋아하는 학생 수, 빈칸수, x, y) 형태로 저장
                                                  -> 정렬해서 조건에 맞는 자리 찾음

                                            없으면 -> 주변에 빈칸이 제일 많은 칸 찾음 (pos2blank 사용)
 - 
'''
def check_outside(x, y):
    if x < 0 or x >= N or y < 0  or y >= N:
        return False
    return True


def generate_pos2blank(): # 초기에 pos2blank 생성
    for x in range(N):
        for y in range(N):
            if 0 < x < N - 1 and 0 < y < N - 1:
                pos2blank[(x, y)] = 4
            elif (x == 0 or x == N - 1) and (y == 0 or y == N - 1):
                pos2blank[(x, y)] = 2
            else:
                pos2blank[(x, y)] = 3


def search_seat():
    seats = set()
    for p in like:
        if p in student_to_pose:
            x, y = student_to_pose[p]
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if not check_outside(nx, ny):
                    continue
                if graph[nx][ny] == 0:
                    seats.add((nx, ny))
    return seats


def calculate_score():
    answer = 0
    for x in range(N):
        for y in range(N):
            p = graph[x][y]
            cnt = 0
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if not check_outside(nx, ny):
                    continue
                if graph[nx][ny] in student_to_like[p]:
                    cnt += 1
            if cnt == 1:
                answer += 1
            elif cnt == 2:
                answer += 10
            elif cnt == 3:
                answer += 100
            elif cnt == 4:
                answer += 1000
    return answer


def allocate_seat(x, y):
    graph[x][y] = p
    student_to_pose[p] = (x, y)

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if not check_outside(nx, ny):
            continue
        pos2blank[(nx, ny)] -= 1


N = int(input())
graph = [[0] * N for _ in range(N)]
dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

pos2blank = {}
generate_pos2blank()
student_to_like = {}
student_to_pose = {}

for k in range(N * N):
    temp = list(map(int, input().rstrip().split()))
    p, like = temp[0], temp[1:]
    student_to_like[p] = like
    seats = search_seat()
    if not seats:
        blank = list(pos2blank.items())
        blank.sort(key=lambda x: (-x[1], x[0][0], x[0][1]))
        for pos, cnt in blank:
            x, y = pos
            if graph[x][y] == 0:
                break
    else:
        seat = []
        for x, y in seats:
            cnt = 0
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if not check_outside(nx, ny):
                    continue
                if graph[nx][ny] in like:
                   cnt += 1
            seat.append([cnt, pos2blank[(x, y)], x, y])
        seat.sort(key=lambda x: (-x[0], -x[1], x[2], x[3]))
        x, y = seat[0][2:]
        allocate_seat(x, y)


print(calculate_score)

