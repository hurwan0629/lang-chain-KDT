# 프로그래머스 배달 문제
# 레벨 2 문제
# https://school.programmers.co.kr/learn/courses/30/lessons/12978


# 마을 50개 이하
# 도로는 2000개 이하
# 
# road는 [[마을1, 마을2, 거리], ...]
# 
# K는 500_000 이하

# # # # # [풀이 전략] # # # # #
# 
# 1. 각 노드까지 걸리는 시간에 대해서 먼저 모두 탐색한다음에 저장한다 
#   (마을번호를 인덱스로하는 리스트를 만들어 리스트에 거리를 저장한다)
# 
# 2. 순회하며 K보다 작은 마을을 모두 선택한다 
# 
# # # # # # # # # # # # # # # 
# 
# 일단 위 작업을 하려면 모든 노드까지의 거리를 알아야한다.
# 
# 다익스트라 알고리즘을 사용하면 
# 0. 길이 N(마을 개수)짜리 배열 만들기 (500_000으로 초기화)
# 1. 시작 노드 잡기 (우선순위 큐(힙)에 넣기)
# 2. 우선순위큐를 다 쓸때까지 적은 방향을 계속 탐색/갱신 해나간다.
# 
# # # # # [문제점과 해결] # # # # #
# 
# 문제에서 리스트를 무작위로 먼저 주기때문에 이를 먼저 정리할 필요가 있다.
# 
# 리스트 형태로 만들어 마을의 인덱스 번호에 [(갈수있는 마을, 비용), ...] 형태로 정리하고 시작하면 될 것 같다.
# 
# # #           [끝]           # # #

import heapq

def solution(N, road, K):
    answer = 0

    # 0. 길이 N+1짜리 배열 만들기 (시작이 1이라서)
    # 최대 길이로 설정해놓기
    town_dist = [500_001 for _ in range(N+1)]
    town_dist[1] = 0

    town_road = [[] for _ in range(N+1)]
    # 마을별로 연결되어있는 길들 정리하기
    for [a, b, r] in road:
        town_road[a].append((r, b))
        town_road[b].append((r, a))
    
    # 가장 짧은것부터 사용할 자료구조로 heapq 사용하기
    # 짧은걸 먼저 쓰면 거리 갱신 비용이 덜 들 수 있음

    # 시작은 항상 1이기 때문에 1로 시작
    left_towns = [(0, 1)]


    while left_towns:
        # 들어오면 값 꺼내기 (기본이 최소힙)
        curr_dist, curr_town = heapq.heappop(left_towns)

        # town_road에서 갈 수 있는 길들 모두 순회하기
        for dist, town in town_road[curr_town]:
            new_dist = curr_dist+dist
            # 다음 동네의 기존 비용보다 적으면 
            if new_dist < town_dist[town]:
                # 갱신하고 새로 계산해주기
                town_dist[town] = new_dist
                # 그리고 다시 계산 대상에 넣어주기
                heapq.heappush(left_towns, (new_dist, town))
    
    # [확인용 로그]
    # for index, dist in enumerate(town_dist):
    #     if dist < 500_001:
    #         print(f"마을{index:2d}: {dist}")

    # 순회하면서 가능한 개수 찾기
    for dist in town_dist:
        if dist <= K:
            answer+=1
            

    return answer