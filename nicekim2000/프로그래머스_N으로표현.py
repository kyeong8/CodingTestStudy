# 와 어렵네
# ex) dp[5]=dp[1]+-*/(4444,-4444) + dp[2]+-/*(444,-444) + dp[3]-+/*(44,-44) + dp[4]+-/*(4,-4)
# 4444, 444, 44 ,4 가 number일때도 생각해줘야함

def solution(N, number):
    if N==number: return 1
    num_dict = {}
    i = 1
    temp = N
    while True:
        num_dict[i] = set([temp,-temp])
        temp = temp * 10 + N
        i += 1
        if temp==number : return i
        if i==9 : break
    for i in range(1,8):
        value=N
        for j in range(i,0,-1):

            for nn in num_dict[j]:
                one = nn + value
                two = nn - value
                three = nn * value
                four = nn // value
                if number in [one, two, three, four]:
                    return i+1
                num_dict[i+1].add(one)
                num_dict[i+1].add(two)
                num_dict[i+1].add(three)
                num_dict[i+1].add(four)
            value = value * 10 + N
    return -1


print(solution(4, 31))
