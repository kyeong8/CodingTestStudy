# 최소비용 구하기
# 다익스트라 알고리즘 분류 문제
# 골드 5
# 다익스트라 오랜만이라 풀 수 있나 도전
# LG CNS 코테 준비중
# 16:16 시작

import heapq
import sys

def di(start):
    dist = [INF for _ in range(n + 1)]

    q = []
    heapq.heappush(q, (0, start))
    dist[start] = 0

    while q:
        distance, node = heapq.heappop(q)
        if dist[node] < distance: continue
        for temp_dist, temp_node in graph[node]:
            cost = temp_dist + distance
            if cost < dist[temp_node]:
                dist[temp_node] = cost
                heapq.heappush(q, (cost, temp_node))
    return dist

input = sys.stdin.readline

n ,m,x= map(int,input().split())

INF = 1e9
graph = [[] for _ in range(n + 1)]
for _ in range(m):
    a, b, value = map(int, input().split())
    graph[a].append((value, b))
x_dist=di(x)
for i in range(1,n+1):
    temp_dist=di(i)
    x_dist[i]+=temp_dist[x]
print(max(x_dist[1:]))

