# 상 하 우 좌
def shark_move(shark):
    sr,sc,ss,sd=shark[:4]
    if sd==0 :
        remain_distance=ss-sr
        No_turn=False
        if remain_distance <= 0 :
            No_turn=True
        remain=remain_distance%(2*r-2)
        if remain <= (r-1) :
            if not No_turn:
                shark[3]=1
            shark[0]=remain
        else:
            shark[0]=r-(remain-(r-1))-1
    elif sd==1:
        remain_distance=ss-(r-sr-1)
        No_turn=False
        if remain_distance <= 0 :
            No_turn=True
        remain=remain_distance%(2*r-2)
        if remain <= (r-1) :
            if not No_turn:
                shark[3]=0
            shark[0] = r - remain - 1
        else:
            shark[0] = remain-(r-1)
    elif sd==2:
        remain_distance = ss - (c-sc-1)
        No_turn=False
        if remain_distance <= 0 :
            No_turn=True
        remain = remain_distance % (2 * c - 2)
        if remain <= (c - 1):
            if not No_turn:
                shark[3] = 3
            shark[1] = c - remain - 1
        else:
            shark[1] = remain-(c-1)
    else:
        remain_distance = ss - sc
        No_turn=False
        if remain_distance <= 0 :
            No_turn=True
        remain = remain_distance % (2 * c - 2)
        if remain <= (c - 1):
            if not No_turn:
                shark[3] = 2
            shark[1] = remain
        else:
            remain-=(c-1)
            shark[1] = c-remain-1
    return shark

def whois(dict,temp):
    if (temp[0],temp[1]) in dict:
        temp2=dict[(temp[0],temp[1])]
        if temp2[4] < temp[4]:
            dict[(temp[0], temp[1])]=temp
    else:
        dict[(temp[0], temp[1])] = temp
    return dict



r,c,m=map(int,input().split())
sharks=[]
for _ in range(m):
    shark=list(map(int,input().split()))
    shark[0]-=1
    shark[1]-=1
    shark[3]-=1
    sharks.append(shark)
sum_value=0
for i in range(c):
    min_shark=r
    new_shark=[]
    temp=[]
    new_shark_dict={}
    # 낚시 후 새로운 상어 집합에 들어갈때 이동까지 해서 들어감
    while sharks:
        temp_shark=sharks.pop()
        if temp_shark[1]==i:
            if temp_shark[0]<min_shark:
                if min_shark!=r:
                    temp=shark_move(temp)
                    new_shark_dict=whois(new_shark_dict,temp)
                min_shark=temp_shark[0]
                temp=temp_shark[:]
            else :
                new_shark_dict=whois(new_shark_dict,shark_move(temp_shark))
        else:
            new_shark_dict = whois(new_shark_dict, shark_move(temp_shark))
    if temp:
        sum_value+=temp[4]
    sharks=list(new_shark_dict.values())
    # for i in range(len(sharks)):
    #     print(sharks[i])
print(sum_value)


