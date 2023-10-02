from collections import deque
import copy
def bfs(n,r,c,visited,value):
    queue=deque([])
    prev={}
    queue.append((r,c))
    dr,dc=[-1,0,1,0],[0,1,0,-1]
    visited[r][c]=1
    group=[(r,c)]
    while queue:
        r,c=queue.popleft()
        for i in range(4):
            new_r,new_c=r+dr[i],c+dc[i]
            if new_r < 0 or new_r >=n or new_c < 0 or new_c >=n: continue
            if visited[new_r][new_c]==1 : continue
            if zido[new_r][new_c]!=value : continue
            group.append((new_r,new_c))
            visited[new_r][new_c]=1
            queue.append((new_r,new_c))
    return visited,group

def score_calc(list1,list2,n,zido):
    list1_value=zido[list1[0][0]][list1[0][1]]
    list2_value = zido[list2[0][0]][list2[0][1]]
    dr, dc = [-1, 0, 1, 0], [0, 1, 0, -1]
    count=0
    for r,c in list1:
        for i in range(4):
            new_r, new_c = r + dr[i], c + dc[i]
            if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n: continue
            if (new_r,new_c) in list2: count+=1
    return (len(list1)+len(list2))*list1_value*list2_value*count

n=int(input())
zido=[]
for cc in range(n):
    zido.append(list(map(int,input().split())))

whole_score=0
###### 3회전이라 3번 반복이 아니라 4번 반복해야하 ㅁㅋㅋㅋㅋ
for _ in range(4):
    visited=[[0 for _ in range(n)] for _ in range(n)]
    g_count=1
    group={}
    for i in range(n):
        for j in range(n):
            if visited[i][j]==0:
                visited,g=bfs(n,i,j,visited,zido[i][j])
                group[g_count]=g
                g_count+=1
    # print(group)
    for i in range(1,g_count):
        for j in range(i+1,g_count):
            whole_score+=score_calc(group[i],group[j],n,zido)
    if cc==3 : break
    middle=n//2
    new_zido=[[0 for _ in range(n)]for _ in range(n)]

    # 십자 돌리기
    for i in range(n):
        for j in range(n):
            # 왼쪽 가운데
            if i==middle:
                new_zido[i][j]=zido[j][i]
            elif j==middle:
                new_zido[i][j]=zido[j][n-1-i]

    # 나머지 돌리기
    region1=[x[:middle] for x in zido[:middle]] # 왼쪽 위
    region2=[x[middle+1:] for x in zido[:middle]]  # 오른쪾 위
    region3=[x[:middle] for x in zido[middle+1:]] # 왼쪽 아래
    region4=[x[middle+1:] for x in zido[middle+1:]] # 오른쪽 아래

    for i in range(middle):
        for j in range(middle):
            new_zido[i][j] = region1[middle - j - 1][i]
            new_zido[i][j+middle+1] = region2[middle - j - 1][i]
            new_zido[i + middle + 1][j] = region3[middle - j - 1][i]
            new_zido[i+ middle + 1][j + middle + 1] = region4[middle - j - 1][i]
    zido=copy.deepcopy(new_zido)
    # for i in range(n):
    #     print(new_zido[i])
print(whole_score)