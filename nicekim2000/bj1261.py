from collections import deque
import sys
input=sys.stdin.readline
n, m = map(int, input().split())
zido=[]
for i in range(m):
    temp=input()
    num=[int(t) for t in temp[:-1]]
    zido.append(num)

visited=[[-1 for _ in range(n)] for _ in range(m)]
q=deque([])
visited[0][0]=0
q.append((0,0))
dr,dc=[0,1,0,-1],[-1,0,1,0]
min_value=1e9
if n==1 and m==1 :
    print(0)
    exit()
while q:
    r,c=q.popleft()
    for i in range(4):
        new_r,new_c=r+dr[i],c+dc[i]
        if new_r < 0 or new_r >=m or new_c < 0 or new_c >=n : continue
        if visited[new_r][new_c] != -1 : continue
        if new_r==m-1 and new_c==n-1 :
            print(visited[r][c])
            exit()
        if zido[new_r][new_c]==1:
            visited[new_r][new_c]=visited[r][c]+1
            q.append((new_r,new_c))
        else :
            visited[new_r][new_c]=visited[r][c]
            q.appendleft((new_r,new_c))
# print(zido[m-1][n-1])