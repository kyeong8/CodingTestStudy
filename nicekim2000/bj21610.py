def check_side(r,c):
    dr,dc=[-1,-1,1,1],[-1,1,1,-1]
    count=0
    for i in range(4):
        new_r,new_c=r+dr[i],c+dc[i]
        if new_r < 0 or new_r >= n or new_c < 0 or new_c >=n:
            continue
        if zido[new_r][new_c]>=1:
            count+=1
    return count

n,m=map(int,input().split())
zido=[]
for _ in range(n):
    zido.append(list(map(int,input().split())))
move=[]
for _ in range(m):
    move.append(list(map(int, input().split())))
cloud=[[n-1,0],[n-1,1],[n-2,0],[n-2,1]]
# 좌 부터 45씩 증가
cloud_dr=[0,-1,-1,-1,0,1,1,1]
cloud_dc=[-1,-1,0,1,1,1,0,-1]
for i in range(m):
    dir=move[i][0]-1
    count=move[i][1]
    move_dr=cloud_dr[dir]*count
    move_dc=cloud_dc[dir]*count
    # 구름 이동 후 물 뿌리기
    is_cloud={}
    for c in cloud:
        c[0]=(c[0]+move_dr)%n
        c[1]=(c[1]+move_dc)%n
        zido[c[0]][c[1]]+=1
        is_cloud[(c[0],c[1])]=1
    for c in cloud:
        zido[c[0]][c[1]]= zido[c[0]][c[1]]+check_side(c[0],c[1])
    new_cloud=[]
    for r in range(n):
        for c in range(n):
            if zido[r][c]>=2 and (r,c) not in is_cloud:
                new_cloud.append([r,c])
                zido[r][c]-=2
    cloud=new_cloud[:]
sum_value=0
for i in range(n):
    sum_value+=sum(zido[i])
    # print(zido[i])
print(sum_value)

