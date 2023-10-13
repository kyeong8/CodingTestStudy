import heapq

n=int(input())
students=[]
students_dict={}
for _ in range(n*n):
    st=list(map(int,input().split()))
    students_dict[st[0]]=st[1:]
    students.append(st)
zido=[[0 for _ in range(n)]for _ in range(n)]
# zido[n//2][n//2]=students[0][0]
dr,dc=[0,0,1,-1],[1,-1,0,0]
for i in range(n*n):
    student=students[i][0]
    like_list=students[i][1:]
    h=[]
    for r in range(n):
        for c in range(n):
            if zido[r][c]==0:
                blank_count=0
                count=0
                for j in range(4):
                    new_r,new_c=r+dr[j],c+dc[j]
                    if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n : continue
                    if zido[new_r][new_c]==0:
                        blank_count+=1
                    elif zido[new_r][new_c] in like_list:
                        count+=1
                heapq.heappush(h,(-count,-blank_count,r,c))
    answer=heapq.heappop(h)
    zido[answer[2]][answer[3]]=student
sum_value=0
for r in range(n):
    for c in range(n):
        count=0
        for j in range(4):
            new_r, new_c = r + dr[j], c + dc[j]
            if new_r < 0 or new_r >= n or new_c < 0 or new_c >= n: continue
            if zido[new_r][new_c] in students_dict[zido[r][c]]:
                count+=1
        if count>0:
            sum_value+=10**(count-1)
print(sum_value)



