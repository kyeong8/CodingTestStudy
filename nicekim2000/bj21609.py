
def find_group(r,c,visited):
    q=[(r,c)]
    value=zido[r][c]
    dr=[0,0,1,-1]
    dc=[1,-1,0,0]
    count=1
    rainbow=[]
    visited_list=[(r,c)]
    while q:
        nr,nc=q.pop()
        for i in range(4):
            new_r,new_c=nr+dr[i],nc+dc[i]
            if new_r < 0 or new_c < 0 or new_c >=n or new_r >= n : continue
            if (zido[new_r][new_c]== value or zido[new_r][new_c]==0) and visited[new_r][new_c]==0:
                count+=1
                if zido[new_r][new_c]==0:
                    rainbow.append((new_r,new_c))
                visited[new_r][new_c]=1
                q.append((new_r,new_c))
                visited_list.append((new_r,new_c))
    for rr,rc in rainbow:
        visited[rr][rc]=0
    return visited,count,visited_list,len(rainbow)

def gravity():
    global zido
    for i in range(n):
        count = 0
        stack = []
        for j in range(n):

            if zido[j][i]!=-2:
                stack.append(zido[j][i])
            count+=1
            if zido[j][i]==-1:
                for k in range(count):
                    if stack:
                        value = stack.pop()
                    else:
                        value = -2
                    zido[j - k][i] = value
                stack=[]
                count=0
        for k in range(count):
            if stack:
                value = stack.pop()
            else:
                value = -2
            zido[j - k][i] = value





n,m=map(int,input().split())
zido=[]
for _ in range(n):
    zido.append(list(map(int,input().split())))
sum_value=0
while True:
    # print("처음 값")
    # for row in zido:
    #     for val in row:
    #         if val==-2 : val=" "
    #         print(f"{val:>5}", end='')  # 오른쪽 정렬로 5자리로 각 값을 출력합니다.
    #     print()  # 다음 행으로 이동합니다.

    leader=[-1,-1]
    max_value=0
    max_rain=0
    visited=[[0 for _ in range(n)] for _ in range(n)]
    visited_list=[]
    for i in range(n):
        for j in range(n):
            if visited[i][j]==0 and zido[i][j]>=1:
                visited[i][j]=1
                visited,value,temp,rainbow=find_group(i,j,visited)
                if value > max_value :
                    max_value=value
                    if value>=2:
                        leader=[i,j]
                    visited_list=temp[:]
                    max_rain=rainbow
                elif value==max_value and rainbow>max_rain:
                    max_value=value
                    if value>=2:
                        leader=[i,j]
                    visited_list=temp[:]
                    max_rain=rainbow
                elif value==max_value and rainbow==max_rain and i>leader[0]:
                    max_value=value
                    if value>=2:
                        leader=[i,j]
                    visited_list=temp[:]
                    max_rain=rainbow
                elif value == max_value and rainbow == max_rain and i == leader[0] and j > leader[1]:
                    max_value=value
                    if value>=2:
                        leader=[i,j]
                    visited_list=temp[:]
                    max_rain=rainbow
    if [-1,-1]==leader : break
    # print(leader)
    # print(max_value)
    # print(sum_value)
    sum_value+=max_value*max_value
    for vr,vc in visited_list:
        zido[vr][vc]=-2
    # print("최대 그룹 제거")
    # for row in zido:
    #     for val in row:
    #         if val==-2 : val=" "
    #         print(f"{val:>5}", end='')  # 오른쪽 정렬로 5자리로 각 값을 출력합니다.
    #     print()  # 다음 행으로 이동합니다.

    gravity()

    # print("중력적용")
    # for row in zido:
    #     for val in row:
    #         if val==-2 : val=" "
    #         print(f"{val:>5}", end='')  # 오른쪽 정렬로 5자리로 각 값을 출력합니다.
    #     print()  # 다음 행으로 이동합니다.

    new_zido=[[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_zido[i][j]=zido[j][n-i-1]
    zido=[x[:] for x in new_zido]
    # 90도 회전
    # print("90도 회전")
    # for row in zido:
    #     for val in row:
    #         if val==-2 : val=" "
    #         print(f"{val:>5}", end='')  # 오른쪽 정렬로 5자리로 각 값을 출력합니다.
    #     print()  # 다음 행으로 이동합니다.

    gravity()
    # print("중력적용")
    # for row in zido:
    #     for val in row:
    #         if val==-2 : val=" "
    #         print(f"{val:>5}", end='')  # 오른쪽 정렬로 5자리로 각 값을 출력합니다.
    #     print()  # 다음 행으로 이동합니다.

print(sum_value)