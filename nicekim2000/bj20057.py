n=int(input())
zido=[]
for _ in range(n):
    zido.append(list(map(int,input().split())))

mid=n//2
turn=[]
left_pos=[n//2,n//2-1]
mid_pos=[n//2,n//2]
dr,dc=[-1,1,1],[1,1,-1]
for i in range(1,mid+1):
    for j in range(3):
        new_pos=[mid_pos[0]+dr[j]*i,mid_pos[1]+dc[j]*i]
        turn.append(new_pos)
    turn.append([left_pos[0]+(-1*(i-1)),left_pos[1]+(-1*(i-1))])
print(turn)
dr,dc=[0,1,0,-1],[-1,0,1,0]
dir=0
while True:
    if mid_pos in turn :
        dir=(dir+1)%4

    mid_pos=[mid_pos[0]+dr[dir],mid_pos[1]+dc[dir]]
    print(mid_pos)



    if mid_pos==[0,0]:
        break