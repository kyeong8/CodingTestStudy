# 해멨던 부분 -> 제초제를 종료조건에 만족하면 그 자리에 뿌리고 종료인데 바로 종료해버림
# 아예 나무가 없는 칸은 skip하면 안되더라고요 
# 나무없는 칸도 검사하기

import copy
def printzido():
    newnew=copy.deepcopy(zido)
    for kkk in list(killer.keys()):
        rr,cc=kkk
        value=killer[kkk]
        newnew[rr][cc]=value*-1-1
    for i in range(n):
        print(newnew[i])
    print()
    for i in range(n):
        print(zido[i])

n,m,k,c=map(int,input().split())
zido=[]
for _ in range(n):
    zido.append(list(map(int,input().split())))
killer={}
whole_kill=0
for _ in range(m):
    # 나무 성장일기
    # 하,우 만 검사해서 진행
    for i in range(n):
        for j in range(n):
            # 나무가 있다면
            if zido[i][j]>=1:
                if i+1 < n and zido[i+1][j]>=1:
                    zido[i][j]+=1
                    zido[i+1][j]+=1
                if j+1 < n and zido[i][j+1]>=1:
                    zido[i][j]+=1
                    zido[i][j+1]+=1

    # print("after grow")
    # printzido()
    # print()

    new_zido=[[0 for _ in range(n)]for _ in range(n)]
    dr=[0,0,1,-1]
    dc=[1,-1,0,0]
    #나무 번식일기
    for i in range(n):
        for j in range(n):
            if zido[i][j]>=1 :
                new_zido[i][j]=zido[i][j]
                count=0
                pos=[]
                child=0
                for a in range(4):
                    new_r=i+dr[a]
                    new_c=j+dc[a]
                    if new_r < 0 or new_r >= n or new_c < 0 or new_c >=n : continue
                    if zido[new_r][new_c]==-1  or zido[new_r][new_c]>=1 :
                        continue
                    if (new_r,new_c) in killer and killer[(new_r,new_c)]>=1: continue

                    # cant=False
                    # for kill in killer:
                    #     if new_r==kill[0] and new_c==kill[1] :
                    #         cant=True
                    #         break
                    # if cant : continue
                    pos.append((new_r,new_c))
                    count+=1
                if count>=1:
                    child=zido[i][j]//count
                    for pr,pc in pos:
                        new_zido[pr][pc]+=child
            elif zido[i][j]==-1: new_zido[i][j]=-1

    zido=copy.deepcopy(new_zido)

    # print("after baby")
    # printzido()
    # print()

    # 제조제 턴
    dr=[-1,-1,1,1]
    dc=[-1,1,-1,1]
    max_kill_count=-1
    max_kill_pos=[]
    for i in range(n-1,-1,-1):
        for j in range(n-1,-1,-1):
            if zido[i][j]==-1 : continue
            tk=k
            if zido[i][j]==0:
                tk=0
            kill_count = zido[i][j]
            kill_pos=[(i,j,c)]
            dk=min(k,tk)
            for a in range(4):
                for b in range(1,dk+1):
                    new_r, new_c = i + dr[a]*b, j + dc[a]*b
                    if new_r < 0 or new_r >= n or new_c < 0 or new_c >=n : break
                    if zido[new_r][new_c]==-1 :break
                    if zido[new_r][new_c]==0 :
                        kill_pos.append((new_r, new_c, c))
                        break
                    kill_count+=zido[new_r][new_c]
                    kill_pos.append((new_r,new_c,c))
            if kill_count>=max_kill_count :
                max_kill_count=kill_count
                max_kill_pos=kill_pos[:]
    whole_kill+=max_kill_count
    # print(max_kill_count)
    # print(max_kill_pos)
    for kk in list(killer.keys()):
        if killer[kk] > 1: killer[kk]-=1
        elif killer[kk]==1 :
            del killer[kk]
    for p in max_kill_pos:
        kr,kc=p[0],p[1]
        zido[kr][kc]=0
        killer[(kr,kc)]=c

    # for kill in killer:
    #     if kill[2]!=1:
    #         max_kill_pos.append((kill[0],kill[1],kill[2]-1))

    # killer=max_kill_pos[:]

    # print("after kill")
    # printzido()
    # print()
    # print(killer)
    # print(whole_kill)


print(whole_kill)