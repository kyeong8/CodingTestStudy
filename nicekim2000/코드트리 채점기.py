# 2023-09-23
# 코드트리_토드트리 채점기
# 5시간
# 최소힙과 딕셔너리를 조합해서 사용
# 구현, 시뮬레이션
# 깡 구현함 !


# 300에 대한 처리가 중요햇음
# 300을 어떻게 처리하냐에 따라 시간초과가 ㄴ옴
# 대기중인 task를 전체 탐색하면 시간초과
# waiting을 도메인별로 묶어서 도메인 별로 우선순위 비교 ( 도메인의 종류는 300개가 최대이다.)
# 그 외 대기줄이나 채점중 또는 로그를 확인하는 것은 모두 딕셔너리 사용해서 시간을 아낌
import heapq

scoring_machine = []
waiting = {}
waiting_dict = {}
scoring = {}
history = {}
scoring_dict = {}
waiting_num=0

def one(n, u):
    global scoring_machine, waiting, waiting_dict,waiting_num
    scoring_machine=[i for i in range(1, n + 1)]
    heapq.heapify(scoring_machine)
    domain,_=u.split("/")
    waiting[domain]=[]
    heapq.heappush(waiting[domain], (1, 0, u))
    waiting_dict[u] = True
    waiting_num+=1
    return


def two(t, p, u):
    global waiting, waiting_dict,waiting_num
    if u not in waiting_dict:
        waiting_dict[u] = True
        domain, _ = u.split("/")
        if domain not in waiting:
            waiting[domain]=[]
        heapq.heappush(waiting[domain], (p, t, u))
        waiting_num+=1
    return


def three(t):
    global waiting, waiting_dict, scoring, scoring_dict, scoring_machine, history,waiting_num
    if len(scoring_machine) == 0 or waiting_num==0 :
        return
    keys=waiting.keys()
    task_pri=0
    task_time=0
    task_domain=""
    for key in keys:
        if key in scoring_dict: continue
        if key in history and t < history[key][0] + 3 * (history[key][1] - history[key][0]):
            continue
        if not waiting[key] : continue
        task=waiting[key][0]
        if task_pri==0:
            task_pri=task[0]
            task_time=task[1]
            task_domain=task[2].split("/")[0]
        else :
            if task_pri > task[0] :
                task_pri=task[0]
                task_time=task[1]
                task_domain=task[2].split("/")[0]
            elif task_pri==task[0] and task_time > task[1] :
                task_pri = task[0]
                task_time = task[1]
                task_domain = task[2].split("/")[0]
    if task_pri==0: return
    task=heapq.heappop(waiting[task_domain])
    machine_num = heapq.heappop(scoring_machine)
    del waiting_dict[task[2]]
    scoring_dict[task_domain] = True
    scoring[machine_num] = (task_domain, t)
    waiting_num -= 1

    return


def four(end_t, j):
    global scoring, scoring_dict, scoring_machine, history
    if j not in scoring:
        return

    domain, start_t = scoring[j]
    del scoring_dict[domain]
    history[domain] = (start_t, end_t)
    del scoring[j]
    heapq.heappush(scoring_machine, j)
    return


def main(instructions):
    global waiting,waiting_num

    for inst in instructions:
        num = int(inst[0])
        if num == 100:
            one(int(inst[1]), inst[2])
        elif num == 200:
            two(int(inst[1]), int(inst[2]), inst[3])
        elif num == 300:
            three(int(inst[1]))
        elif num == 400:
            four(int(inst[1]), int(inst[2]))
        else:
            print(waiting_num)



q = int(input())
instructions = [input().split() for _ in range(q)]
main(instructions)
