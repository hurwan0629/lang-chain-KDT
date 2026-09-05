# 그리디를 써야할때와 쓰지 말아야할 때
이번 글에서는 그리디 알고리즘을 사용하면 좋은 경우와 사용하면 안되는 경우에 대해서 알아보려 합니다.

## 그리드 알고리즘의 개요
우선 그리디는 알고리즘이라고 하는것과 동시에 문제를 해결하는 **전략** 또는 패턴이라고 하는것이 더 올바르다고 생각합니다.

그리디는 여러 자료구조 또는 문제 상황에서 사용이 가능합니다.
- 스케줄링
- 노선도 길찾기
- 거스름돈
- 파라미터 튜닝 (머신러닝)

그리디 알고리즘의 정의를 간단히 알아보면 매 순간 최적의 해만을 선택하는 알고리즘(패턴)이라고 할 수 있습니다. 이는 직관적으로 보았을 때 매우 간단하지만 극소점/극대점에 갇히기 매우 쉬운 알고리즘이기도 합니다.

일반적으로 그리디 알고리즘은 이산적인 선택 또는 선택 안함에 대한 문제이지만 최적의 해를 찾는다는 점에서 경사 하강법과도 유사한 특징을 가지고 있습니다.

# 문제를 풀어보자
[섬 연결하기](https://school.programmers.co.kr/learn/courses/30/lessons/42861?language=python3)문제를 풀었습니다.
```python
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
```

![섬 연결하기 문제 푼거](https://raw.githubusercontent.com/hurwan0629/lang-chain-KDT/92e42f580251c4317818d78fd5f879d329b28dec/workspace/personal/assignment/05_greed_and_dp/image.png)

> 예이~