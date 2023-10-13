
def bfs(r,c):
    global visited,visited_cnt
    q=[(r,c)]
    visited[r][c]=1
    dr,dc=[1,-1,0,0],[0,0,1,-1]
    cnt=1
    while q:
        nr,nc=q.pop()
        for i in range(4):
            new_r,new_c=nr+dr[i],nc+dc[i]
            if new_r < 0 or new_r >= 2**n or new_c < 0 or new_c >= 2**n: continue
            if zido[new_r][new_c]==0 or visited[new_r][new_c]==1: continue
            visited[new_r][new_c]=1
            cnt+=1
            q.append((new_r,new_c))
    visited_cnt+=cnt
    return cnt



n,q=map(int,input().split())
zido=[]
for _ in range(2**n):
    temp=list(map(int,input().split()))
    zido.append(temp)
ls=list(map(int,input().split()))
dr,dc=[1,0],[0,1]
sum_value=0
for l in ls:
    # 잘라서 원점으로 옮기고 회전후 다시 삽입 과정
    for i in range(0,2**n,2**l):
        for j in range(0,2**n,2**l):
            temp=[x[j:j+(2**l)] for x in zido[i:i+(2**l)]]
            # 다시 삽입
            for r in range(2**l):
                for c in range(2**l):
                    zido[i+r][j+c]=temp[2**l-1-c][r]


    # 주변 얼음량 계산 후 녹을지 말지 결정
    ice=[[0 for _ in range(2**n)] for _ in range(2**n)]
    for r in range(2**n):
        for c in range(2**n):
            if zido[r][c]==0 : continue
            for i in range(2):
                new_r,new_c=r+dr[i],c+dc[i]
                if new_r < 0 or new_r >= 2**n or new_c < 0 or new_c >= 2**n: continue
                if zido[new_r][new_c]>0 :
                    ice[r][c]+=1
                    ice[new_r][new_c]+=1
            if ice[r][c]<3 : zido[r][c]-=1

# sum
for i in range(len(zido)):
    sum_value+=sum(zido[i])
# 최대영역 찾기

visited_cnt=0
max_cnt=0
visited=[[0 for _ in range(2**n)] for _ in range(2**n)]
for r in range(2**n):
    for c in range(2**n):
        if visited[r][c]==0 and zido[r][c]!=0:
            cnt=bfs(r,c)
            if cnt>max_cnt:
                max_cnt=cnt
            if max_cnt>(2**n)*(2**n)-visited_cnt :
                print(sum_value)
                print(max_cnt)
                exit()
        if zido[r][c]==0 : visited_cnt+=1
print(sum_value)
print(max_cnt)