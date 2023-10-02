# 2023-10-?
# 코드트리_싸움땅
# 3시간
# 딕셔너리사용, 총의 정보는 리스트에 담아서 관리
# 구현, 시뮬레이션
# 깡 구현함 !

# dir=상,우,하,좌 순서

n, m, k = map(int, input().split())
zido = []
for _ in range(n):
    numbers = list(map(int, input().split()))
    zido.append([[number] if number != 0 else [] for number in numbers])
players = {}
players_pos = {}
for i in range(1, m + 1):
    temp = list(map(int, input().split()))
    # players[플레이어 번호]=[(r,c),direction,초기능력치,가지고 있는 총의 공격력]
    players[i] = [(temp[0] - 1, temp[1] - 1), temp[2], temp[3], 0]
    players_pos[(temp[0] - 1, temp[1] - 1)] = i
dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
point = [0 for _ in range(m)]
for _ in range(k):
    for key in list(players.keys()):
        player = players[key][:]
        new_r, new_c = player[0][0] + dir[player[1]][0], player[0][1] + dir[player[1]][1]
        if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n:
            # 왔던 방향 반대로 2번 이동
            new_r, new_c = player[0][0] + dir[(player[1]+2)%4][0], player[0][1] + dir[(player[1]+2)%4][1]
            players[key][1]=(player[1]+2)%4
            player[1]=(player[1]+2)%4
        # 해당 칸에 플레이어가 있는 경우
        if (new_r, new_c) in list(players_pos.keys()):

            # 땅 주인 플레이어 소환
            player1 = players[players_pos[(new_r, new_c)]]

            # 침략자 능력치 선언
            player_ability = player[2]
            player_gun = player[3]
            player_sum = player_ability + player_gun

            # 땅 주인 능력치 선언
            player1_ability = player1[2]
            player1_gun = player1[3]
            player1_sum = player1_ability + player1_gun

            # 전쟁해서 승자 찾기
            move_player = []
            move_player_key = 0
            win_player = []
            win_player_key = 0
            if player_sum > player1_sum:
                move_player = player1[:]
                move_player_key = players_pos[(new_r, new_c)]
                win_player = player[:]
                win_player_key = key
            elif player_sum < player1_sum:
                move_player = player[:]
                move_player_key = key
                win_player = player1[:]
                win_player_key = players_pos[(new_r, new_c)]
            else:
                if player_ability > player1_ability:
                    move_player = player1[:]
                    move_player_key = players_pos[(new_r, new_c)]
                    win_player = player[:]
                    win_player_key = key
                else:
                    move_player = player[:]
                    move_player_key = key
                    win_player = player1[:]
                    win_player_key = players_pos[(new_r, new_c)]

            # 포인트 정산
            point[win_player_key - 1] += abs(player1_sum - player_sum)

            # 총 버리기
            if move_player[3] >= 1:
                zido[new_r][new_c].append(move_player[3])
                move_player[3] = 0

            # 플레이어 좌표 사전에서 삭제
            del players_pos[(player[0][0], player[0][1])]
            del players_pos[(new_r, new_c)]

            # 패배자 이동 위치 찾기
            loser_dir = move_player[1]
            while True:
                loser_r, loser_c = new_r + dir[loser_dir][0], new_c + dir[loser_dir][1]
                if (loser_r < 0 or loser_r >= n or loser_c < 0 or loser_c >= n) or (loser_r, loser_c) in list(
                        players_pos.keys()):
                    loser_dir = (loser_dir + 1) % 4
                    continue
                else:
                    break
            move_player[1]=loser_dir
            # 패배자 이동 후 좌표 수정
            move_player[0] = (loser_r, loser_c)
            win_player[0] = (new_r, new_c)

            # 패배자가 이동한 칸에 총이 있는지 검사
            if len(zido[loser_r][loser_c]) >= 1:
                guns = zido[loser_r][loser_c]
                guns.sort()
                move_player[3] = guns[-1]
                zido[loser_r][loser_c] = guns[:-1]

            # 승리자는 제일 좋은 총으로 교체
            if len(zido[new_r][new_c]) >= 1:
                guns = zido[new_r][new_c]
                if win_player[3] >= 1:
                    guns.append(win_player[3])
                guns.sort()
                win_player[3] = guns[-1]
                zido[new_r][new_c] = guns[:-1]

            # 플레이어 정보 업데이트
            players[win_player_key] = win_player[:]
            players[move_player_key] = move_player[:]

            # 플레이어 위치 정보 업데이트
            players_pos[(win_player[0][0], win_player[0][1])] = win_player_key
            players_pos[(move_player[0][0], move_player[0][1])] = move_player_key

        # 헤딩 킨에 플레이어가 없는 경우
        else:
            # 총이 있는 경우
            if len(zido[new_r][new_c]) >= 1:
                guns = zido[new_r][new_c]
                # 플레이어가 총이 있는 경우
                if player[3] != 0:
                    guns.append(player[3])
                guns.sort()
                players[key][3] = guns[-1]
                zido[new_r][new_c] = guns[:-1]
            # 플레이어 좌표 사전 업데이트

            del players_pos[(player[0][0], player[0][1])]
            players[key][0] = (new_r, new_c)
            players_pos[(new_r, new_c)] = key
for i in range(len(point)):
    print(point[i],end=' ')
