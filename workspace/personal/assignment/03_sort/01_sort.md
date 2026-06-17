# 탐색
> 탐색은 특정 자료구조, 넓게 보면 특정 공간에서 원하는 데이터 또는 결과를 찾는 과정을 말합니다. 자료구조의 경우에는 선형탐색, 이진탐색, BFS, DFS가 있을 수 있고, 특정 경우의 값 또는 그 수를 찾기 위해서는 다익스트라, 그리디, DP와 함께 앞에서 말한 BFS, DFS 또한 동일하게 사용 가능합니다. 우선 이번 글에서는 과제로 받은 앞의 4가지 탐색 기법에 대해서 알아보겠습니다.

## 선형 탐색
선형 탐색은 구현이 매우 간단한 직관적인 방식입니다. 코드를 통해 표현을 해보면 아래와 같습니다.
```python
random_list = [1, -2, 3, 7, 8, 10, 100, 24, 12]

target = 8

for i in range(len(random_list)):
   if target == random_list[i]:
    print(f"발견/인덱스: {i}")
```
가 됩니다. 정렬이 되어있든 되어있지 않든 `O(n)`의 시간복잡도가 나온다는 특징에 의해 주로 정렬되지 않았으며 인덱스가 없는 경우에 사용하기 좋은 방식입니다.

## 이진 탐색
이진 탐색은 일반적으로 정렬되어 있거나 `왼쪽 자식 < 부모 < 오른쪽 자식` 또는 반대 형태인 이진 탐색 트리인 경우 사용 가능한 탐색 방식입니다.
### 분할 정복 방식
이진 탐색은 정렬되어 있을 때 쉽게 찾을 수 있으며 그 방식은 그냥 중간 지점을 잡고, 그 값과 비교하여 값을 반환하거나 다음 비교 리스트를 재귀적으로 처리하는 것입니다.

간단한 예시는 다음과 같습니다.
```python
import random
from typing import Literal

sorted_list = sorted(random.sample([v for v in range(1, 2000)], 50))


def binary_search(target: int, arr: list[int], order_type: Literal["asc", "desc"] = "asc") -> int:

  if len(arr) <= 0:
    return -1
  head = 0
  tail = len(arr) - 1

  # 핵심
  def divl(h, t):
    # 값을 못찾으면 return
    if h > t:
      return -1
    pivot = (h+t) // 2

    if target < arr[pivot]:
      if order_type == "asc":
        return divl(h, pivot-1)
      else:
        return divl(pivot+1, t)
    
    elif target > arr[pivot]:
      if order_type == "asc":
        return divl(pivot+1, t)
      else:
        return divl(h, pivot-1)
    else:
      return pivot
  
  return divl(head, tail)

target = random.sample([a for a in sorted_list], 1)[0]
print(binary_search(target, sorted_list, "asc"))
print(binary_search(target, sorted(sorted_list, reverse=True), "desc"))
```

### 이진 탐색 트리
이진 탐색 트리의 경우에도 위보다 간단하게 노드를 타고 들어가는 방식입니다. 이번에는 의사 코드를 통해 직관적으로 나타내겠습니다.

```python
class Node():
  pass
class Tree():
  pass
# # 위의 클래스가 구현되어있다고 가정 # #

# 10을 가지고 있는 노드를 탐색한다고 가정
target = 10

tree = Tree()

pointer = tree.root()

# 오름차순 정렬일 경우
while pointer is not None and pointer.value != target: 
  if target < pointer.value:
    pointer = pointer.left
  else:
    pointer = pointer.right

if pointer is not None:
  print(f"발견. 노드 id: {id(pointer)}")
else:
  print("해당 값 존재하지 않음")
```

## BFS와 DFS
`BFS`와 `DFS`는 가장 근본 있고(라고 생각하고) 입문할 때 쉬운 탐색 방식입니다.

`BFS`는 큐를 이용하여 다음 값들을 큐 뒤에 넣고, 앞의 값을 꺼내서 탐색 및 다음 값 큐에 `push`를 반복하는 방식입니다.

`DFS`는 재귀 함수를 통해 값을 찾을 때까지 들어갔다가 반환을 통해 돌아오고, 다시 다른 분기로 들어가서 탐색을 반복하는 방식입니다.

### BFS 구현
대표적인 문제인 이중 리스트에서 BFS를 사용하는 방법이 있습니다.
```python
# GPT한테 받은 미로
  # 0: 이동 가능
  # 1: 벽
maze = [
    [0, 1, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
]

from collections import deque

q = deque([(0, 0)])

i = 1

visited = set(["(0, 0)"])

# BFS는 보통 
while q:
  n = q.popleft()
  print(f"탐색: {n} / {i}번째 탐색")
  i+=1
  x = n[1]
  y = n[0]

  # 출구인지 확인
  if x == len(maze[0])-1 and y == len(maze)-1:
    print("탐색 완료")
    break
  
  # 다음 갈 수 있는 칸들 탐색
  if x-1 >= 0 and (f"({y}, {x-1})" not in visited) and maze[y][x-1] == 0:
    q.append((y, x-1))
    visited.add(f"({y}, {x-1})")
    

  if x+1 < len(maze[0]) and (f"({y}, {x+1})" not in visited) and maze[y][x+1] == 0:
    q.append((y, x+1))
    visited.add(f"({y}, {x+1})")

  if y-1 >= 0 and (f"({y-1}, {x})" not in visited) and maze[y-1][x] == 0:
    q.append((y-1, x))
    visited.add(f"({y-1}, {x})")

  if y+1 < len(maze) and (f"({y+1}, {x})" not in visited) and maze[y+1][x] == 0:
    q.append((y+1, x))
    visited.add(f"({y+1}, {x})")
```
### DFS
DFS는 위와 다른 방식으로 구현하게 됩니다.

```python
# GPT한테 받은 미로
  # 0: 이동 가능
  # 1: 벽
maze = [
    [0, 1, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 1, 0, 1],
    [0, 0, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0],
]

from collections import deque

i = 1

def dfs_maze(y, x, visited: set[tuple[int, int]]):
  global i
  print(f"탐색: ({y}, {x}) / {i}번째 탐색")
  i+=1
  # 출구인지 확인
  if y == len(maze)-1 and x == len(maze[0])-1:
    print("발견!")
    return True
  visited.add((y, x))
  
  # 다음 위치 찾기
  if x-1 >= 0 and ((y, x-1) not in visited) and maze[y][x-1] == 0:
    if dfs_maze(y, x-1, visited):
      return True

  if x+1 < len(maze[0]) and ((y, x+1) not in visited) and maze[y][x+1] == 0:
    if dfs_maze(y, x+1, visited):
      return True

  if y-1 >= 0 and ((y-1, x) not in visited) and maze[y-1][x] == 0:
    if dfs_maze(y-1, x, visited):
      return True

  if y+1 < len(maze) and ((y+1, x) not in visited) and maze[y+1][x] == 0:
    if dfs_maze(y+1, x, visited):
      return True

dfs_maze(0, 0, set())
```
