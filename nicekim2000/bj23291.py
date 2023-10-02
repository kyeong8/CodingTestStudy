# 2023-09-20
# bj23291_어항정리    
# 2시간  
# 깡구현함
# 구현, 시뮬레이션  
# 깡 구현함 

def fishplus(fish):
    min_value=min(fish[0])
    for i in range(len(fish[0])):
        if fish[0][i]==min_value:
            fish[0][i]+=1
    return fish

# 1. 1층에서 바닥에 쌓일 것들을 슬라이싱해서 새로운 1층
# 2. 나머지 굴려질 것들에서 층을 나눠 리스트에 append 
def  rotation(fish):
    index=0
    while True:
        count=index//2
        if len(fish[0])-count-1<len(fish) : break
        newfish=[]
        newfish.append(fish[0][count+1:])
        for i in range(count,-1,-1):
            temp=[]
            for j in range(len(fish)):
                temp.append(fish[j][i])
            newfish.append(temp)
        index+=1
        fish=newfish
    return fish

def fishwar(fish):
    newfish=[]
    for i in range(len(fish)):
        temp=[]
        for j in range(len(fish[i])):
            temp_num=fish[i][j]
            if j-1 >= 0 : temp_num+=return_num(fish[i][j-1],fish[i][j])
            if j+1 <= len(fish[i])-1: temp_num+=return_num(fish[i][j+1],fish[i][j])
            if i-1 >= 0 : temp_num+=return_num(fish[i-1][j],fish[i][j])
            if i+1 <= len(fish)-1:
                if j < len(fish[i+1]): temp_num+=return_num(fish[i+1][j],fish[i][j])
            temp.append(temp_num)
        newfish.append(temp)
    return newfish

def return_num(a,b):
    if (a-b) % 5 ==0 and (a-b)//5 < 0 : return (a-b)//5
    elif (a-b)//5 < 0 : return (a-b)//5 + 1
    else : return (a-b)//5

def serialization(fish):
    newfish=[]
    for i in range(len(fish[0])):
        index=0
        while True:
            if index >= len(fish) or i >= len(fish[index]): break
            newfish.append(fish[index][i])
            index+=1x
    return newfish

def zfold(fish):
    num=len(fish)//4
    a=fish[:num]
    b=fish[num:2*num]
    c=fish[2*num:3*num]
    d=fish[3*num:]
    a.reverse()
    c.reverse()
    newfish=[d,a,b,c]
    return newfish

# 각 층을 리스트로 표현한다
n,k=map(int,input().split())
fish=list(map(int,input().split()))
count=0
while True:
    if max(fish)-min(fish)<=k : break
    fish=[fish]
    fish=fishplus(fish)
    # print(fish) 
    fish=rotation(fish)
    # print(fish)
    fish=fishwar(fish)
    # print(fish)
    fish=serialization(fish)
    # print(fish)
    fish=zfold(fish)
    # print(fish)
    fish=fishwar(fish)
    # print(fish)
    fish=serialization(fish)
    # print(fish)
    
    count+=1
print(count)
