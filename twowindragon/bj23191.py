'''
    - 30분 고민하고 1시간 30분 구현
    - 시간 복잡도 생각 안함, N이 100이하여서 구현만 하면 맞을 것이라고 생각함
    - 가장 중요한 점은 어항을 어떻게 저장할 것인가 -> 행렬을 회전하고 붙이려면 어느 형태가 편할까에 대한 고민을 함
    - 그래서 백준에 나온 그림 기준 아래와 같이 리스트에 저장
       3 5               [[3, 3],
       3 14 9 11 8  -> [14, 5],
                         [9],
                         [11],
                         [8]]
    - 그럼 회전할 때 [[3, 3],   만 뽑아서 90도 회전하고    [[9],  + [[14, 3], 이런식으로 붙이면 됨
                    [14, 5]]                          [11],  +  [5, 3]]
                                                       [8]]
    - 물고기 이동에서 중요한 건 모든 구역에서 동시에 발생하는 것 -> 이동량을 저장할 행렬하나 선언해줘서 저장해놓고 나중에 기존의 어항에 더해주면 됨
'''


import copy


def rotation_90(h, w):
    if len(fishbowl) - w < h: # 오른쪽에 바닥이 없는 경우
        return None
    
    temp = fishbowl[:w]
    new_bowl = fishbowl[w:]
    rotate_bowl = [[0] * w for _ in range(h)] # 회전 후 저장할 공간
    # 90도 회전
    for i in range(w):
        for j in range(h):
            rotate_bowl[j][w - 1 - i] = temp[i][j]
    # 회전 후 바닥에 있는 어항과 합체 (한 번에 요소들을 합치기 위해 extend사용)
    for i in range(h):
        new_bowl[i].extend(rotate_bowl[i])
    return new_bowl


def rotation_180():
    h = len(flatten_fishbowl)
    new_bowl = flatten_fishbowl[h // 2:]
    for i in range(h // 2):
        new_bowl[i].extend(flatten_fishbowl[h//2 - i - 1][::-1])

    return new_bowl


def fish_move(fishbowl):
    # 1 ≤ 각 어항에 들어있는 물고기의 수 ≤ 10,000
    n = len(fishbowl)
    max_fish = 1
    min_fish = 10000
    flatten_fishbowl = []
    # 물고기 이동량 저장 + or -
    diff_bowl = [[0] * len(fishbowl[i]) for i in range(n)]
    
    # 오른쪽과 아래만 비교하면서 이동 값 기록
    for i in range(n):
        for j in range(len(fishbowl[i])):
            if i < n - 1 and len(fishbowl[i+1]) > j:  # 행렬의 형태가 [[1, 2, 3], [1, 2, 3], [1], [1]] 이런 경우가 존재하기 때문에
                d = abs(fishbowl[i][j] - fishbowl[i+1][j]) // 5
                if d > 0:
                    if fishbowl[i][j] > fishbowl[i+1][j]:
                        diff_bowl[i][j] -= d
                        diff_bowl[i+1][j] += d
                    else:
                        diff_bowl[i][j] += d
                        diff_bowl[i + 1][j] -= d
        
            if j < len(fishbowl[i]) - 1:
                d = abs(fishbowl[i][j] - fishbowl[i][j + 1]) // 5
                if d > 0:
                    if fishbowl[i][j] > fishbowl[i][j + 1]:
                        diff_bowl[i][j] -= d
                        diff_bowl[i][j + 1] += d
                    else:
                        diff_bowl[i][j] += d
                        diff_bowl[i][j + 1] -= d

        # 기존의 어항에 물고기 이동량 반영
        for j in range(len(fishbowl[i])):
            fishbowl[i][j] += diff_bowl[i][j]
            if max_fish < fishbowl[i][j]:
                max_fish = fishbowl[i][j]
            elif min_fish > fishbowl[i][j]:
                min_fish = fishbowl[i][j]
            flatten_fishbowl.append([fishbowl[i][j]])
    return flatten_fishbowl, min_fish, max_fish

# 입력 받기
N, K = map(int, input().split())
temp = list(map(int, input().split()))
answer = 1 

while True:
    min_value = min(temp)
    # 최소값에 1씩 더함
    for i in range(N):
        if temp[i] == min_value:
            temp[i] += 1

    # 행렬의 형태를 [[5], [2], [3] .... [8]]
    fishbowl = [[temp[i]] for i in range(N)]
    h, w = 1, 1 # 공중부양 하는 행렬의 형태 높이, 길이

    while True:
        new_bowl = rotation_90(h, w) # 90도 회전 후 어항을 쌓음
        if not new_bowl: # 오른쪽에 있는 어항의 아래에 바닥에 있는 어항이 있을때까지 반복
            break
        fishbowl = copy.deepcopy(new_bowl)
        # 공중 부양해야 하는 행렬의 형태가 (1, 1) (2, 1) (2, 2) (3, 2) ... 이렇게 변함
        if h == w:
            h += 1
        else:
            w += 1

    flatten_fishbowl, _, _ = fish_move(fishbowl) # 물고기 이동

    for _ in range(2): # 반반 작업 두 번
        flatten_fishbowl = rotation_180() # 180도 돌리고 쌓기
        
    flatten_fishbowl, min_fish, max_fish = fish_move(flatten_fishbowl) # 물고기 움직이고, 최대 최소값 구하기
    if max_fish >= min_fish and max_fish - min_fish <= K: # 최대 - 최소 가 K 이하면 종료
        print(answer)
        exit()
    answer += 1

    temp = [i[0] for i in flatten_fishbowl] # 처음 입력 받을 때와 동일하게 변환