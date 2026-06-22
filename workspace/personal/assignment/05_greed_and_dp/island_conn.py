# https://school.programmers.co.kr/learn/courses/30/lessons/42861?language=python3
# 섬 연결하기

# 해결 전략
# 어짜피 하나랑만 이어지면 되기 때문에
# 1. 이어진 섬들을 하나로 보고, 
# 2. 연결 비용이 적은것부터 연결해나간다
# 방식만 지키면 해결이 가능할 것 같다.


def solution(n, costs: list[list[int]]):
    # n: [[섬1, 섬2, 비용], ...] 이기 때문에 비용 순서로 정렬해주기
    costs.sort(key=lambda x: x[2])

    # 연결 상태를 확인하기 위한 좋은 방법?
    # 딕셔너리로 연결 집합 번호를 매겨주기
    new_group = n

    # 그룹_번호: list[소속 섬 번호]
    group: dict[int, list[int]] = {i: [a] for i, a in enumerate(range(n))}

    # 섬: 소속 그룹
    belong = {a: i for i, a in enumerate(range(n))}

    answer = 0

    def bind_group(a, b):
        nonlocal new_group 
        new_group += 1
        # a와 연결된 모든 섬들 선택
        group_a = group.get(belong.get(a))

        # b와 연결된 모든 섬들 선택
        group_b = group.get(belong.get(b))

        # a, b그룹의 소속을 new_group로 바꿔주기
        for i in (group_a + group_b):
            belong[i] = new_group

        # 두 그룹을 새로운 그룹으로 합쳐주기
        group[new_group] = group_a + group_b

    for c in costs:
        # 두 섬이 같은 소속이 아니면 연결해주기
        if belong.get(c[0]) != belong.get(c[1]):
          answer += c[2]
          bind_group(c[0], c[1])
          # 연결 후 모두 연결되어있으면 끝내기
          if len(group.get(new_group)) == n:
              break


    
    return answer



if __name__ == "__main__":
  result = solution(4, [[0,1,1],[0,2,2],[1,2,5],[1,3,1],[2,3,8]])
  print(result)