# [과제] 자원 소모를 나타내는 빅오 표기법
이번에는 시간 복잡도와 공간 복잡도, 그리고 이를 나타내기 위한 빅오(Big-O) 표기법에 대한 공부를 하라는 선생님의 과제가 있었습니다. 따라서 이번에는 자료구조/알고리즘 등의 시간/공간 복잡도를 정리해 본 뒤, 이를 잘 활용하는 방법에 대해서 이야기를 해보겠습니다.

## 시간 복잡도와 공간 복잡도, 빅오 표기법
우선 개발에서는 빅오(Big-O) 표기법을 자주 사용하게 됩니다. 일반적으로 자료구조 또는 알고리즘을 사용하는 경우에는 그 방법을 실천하기 위한 시간과 공간을 사용해야 합니다. 일반적으로 시간의 경우에는 CPU의 연산과 연관되어 있고, 공간의 경우에는 사용하는 메모리와 연관되어 있습니다. 이는 기초적인 개발을 할 경우에는 그 크기가 미미하여 학생의 경우에는 간과하기 쉽지만 실제 서비스를 돌릴 시 몇십, 몇백만 명의 트래픽을 감당하거나 머신러닝을 위한 압도적인 양의 연산을 해야 하는 경우 이러한 사소한 차이가 성능의 차이를 만들게 됩니다.

### 빅오 표기법
위에서 말한 수식의 경우, 일반적으로 `a*n^2 + b*n + c*log n + k`와 같은 수식으로 알고리즘과 자료구조에 쓰이는 자원의 양을 표시할 수 있습니다. 하지만 결국 `n`이 커질수록 최고차항 이외의 항들은 모두 큰 의미를 갖지 못하기 때문에 빅오 표기법에서는 최고차항만을 보여주는 방식으로 성능을 나타냅니다.

예를 들어 리스트를 순회하며 최댓값을 구하는 경우에는 `an + b`이라는 초깃값을 설정하는 비용(`b`)이 들지만 이는 `n`(리스트의 길이)가 길어질수록 무의미해지기 때문에 `O(n)`으로 표현하게 됩니다.

## 자료구조
자료구조는 기본적으로 삽입/삭제/탐색/접근/공간의 요소가 트레이드 오프 관계로 형성됩니다. 예시로 배열의 경우에는 인덱스를 통한 접근을 통해 `O(1)`로 접근이 가능하지만 삽입을 위해서는 `O(n)`의 공간과 시간 복잡도가 필요합니다. (일반적인 배열의 경우에는 리스트를 복사하여 새로 만듭니다.) 반대로 연결 리스트의 경우에는 순차적으로 데이터를 타고 올라가며 값을 찾기 때문에 `O(n)`이라는 탐색 시간이 걸리지만 삽입과 삭제에는 위치를 안다는 가정하에 `O(1)`의 시간 복잡도가 걸리게 되며, 공간 또한 `O(1)`만을 요구하게 됩니다.

## 알고리즘
알고리즘 또한 자료구조와 트레이드 오프의 특성이 거의 동일합니다. 대체로 예시로 많이 등장하는 정렬의 경우, 병합 정렬의 경우에는 `O(n log n)`의 시간과 `O(n)`의 공간 복잡도를 요구하지만 선택 정렬의 경우에는 `O(n^2)`의 시간과 `O(1)`의 공간 복잡도를 씁니다. 경우에 따라 평균과 최악의 경우가 다른 정렬이 존재하여 그 특성을 잘 고려해야 합니다.

## 시간 복잡도별 예시들
이번에는 시간 복잡도별 대표적인 자료구조 또는 알고리즘을 작성하여 그 형태를 구체적으로 알아보겠습니다.
### O(1) 
일반적으로 인덱스 또는 해시를 통해 주소에 직접 접근이 가능한 방식입니다.
```python
arr = [1, 2 , 3, 4, 5]
dic = {"one": "1", "two": "2", "three": "3"}

print(arr[3])
# 해시를 위한 연산은 시간 복잡도의 규칙에 따라 생략됩니다.
print(dic["one"])

from collections import deque

q = deque([1, 2, 3])
print(q.pop())
print(q.popleft())
```
### O(log n)
대표적으로 트리의 경우, `n`이 많아질수록 점점 레벨의 증가 속도가 낮아지고, 정렬되었을 경우 탐색의 범위가 줄며 효율적인 `O(log n)`의 형태를 나타냅니다.
```python
# # # # # # # # 탐색을 위한 트리 만들기 (트리 라이브러리 찾아보긴 그렇고 그냥 직접 구현하는 게 좋겠다 느꼈습니다) # # # # # # # # 
from collections import deque

class Node:
  def __init__(self, value):
    self.value = value
    self.left = None
    self.right = None

first = Node(10)

q = deque([first])

# 트리에 더미데이터 넣기 (큐의 활용 예시)
for i in range(20):
  n = q.popleft()
  n.left = Node(i*5)
  n.right = Node(i*14)
  q.append(n.left)
  q.append(n.right)

# # # # # # # # 길어지긴 했지만 사전 준비 과정 # # # # # # # # 

# 탐색을 위한 초기화
q = deque([first])

# 아래 과정이 
while True:
  n = q.popleft()
  if n is None:
    continue
  # 목표값: 14*18
  if n.value == 14*18:
    print("발견")
  elif len(q) == 0:
    print("탐색 실패")
    break
```
가 될 수 있습니다.

### O(n)
일반적인 선형 탐색이 `O(n)`을 보여주게 됩니다.
```python
import random

l = [i for i in range(1, random.randint(100, 200))]

target = random.randint(1, len(l))

for i in range(len(l)):
  if(target == l[i]):
    print(f"탐색 횟수: {i+1}")
```
### O(n log n)
효율적인 정렬들에서 위와 같은 수치가 나오게 됩니다. (병합, 퀵 등)
```python
target_l = [8, 3, 5, 2, 7, 1, 4, 6]

def merge_sort(l: list):
  if len(l) <= 1:
    return l
  
  left = merge_sort(l[0:len(l)//2])
  right = merge_sort(l[len(l)//2:])

  merged_l = []
  l_index = 0
  r_index = 0

  while l_index < len(left) and r_index < len(right):
    if left[l_index] <= right[r_index]:
        merged_l.append(left[l_index])
        l_index += 1
    else:
        merged_l.append(right[r_index])
        r_index += 1

  merged_l += left[l_index:]
  merged_l += right[r_index:]

  return merged_l


print(merge_sort(target_l))
```
입니다.
### O(n^2)
느린 편의 정렬이 위와 같은 시간 복잡도를 가지는 경우가 많습니다. 예를 들면 순회를 `n`번 하며 최솟값을 순서대로 정렬하는 선택 정렬이 있습니다.

```python
target_l = [8, 3, 5, 2, 7, 1, 4, 6]

for i in range(len(target_l)):
  # i번째 인덱스 탐색
  # 최솟값 지정
  target = target_l[i]
  target_index = i

  for j in range(i, len(target_l)):
    if target > target_l[j]:
      target = target_l[j]
      target_index = j
  
  # 위치 변환
  tmp = target_l[i]
  target_l[i] = target
  target_l[target_index] = tmp

print(target_l)
```
### O(2^n)
`n`이 증가함에 따라 연산 횟수가 2배씩 늘어나는 구조입니다.
```python
# 모든 조합의 경우를 보는 경우
arr = [1, 2, 3, 4]

def find_all_kind(l: list):
  if len(l) == 1:
    return l
  for v in l:
    print([v] +  find_all_kind(l[1:]))
```

### O(n!)
모든 순서를 고려하여 뽑는 경우입니다.
```python
arr = [1, 2, 3, 4]

def make_order(current_arr, target_arr):

  # 완성되었다면 반환해주기
  if len(current_arr) == len(target_arr):
    print(current_arr)
    return
  # 완성되지 않았다면 그 뒤에 계속 추가하기
  for num in target_arr:
    if num in current_arr:
        continue
    current_arr.append(num)
    make_order(current_arr, target_arr)
    current_arr.pop()

make_order([], arr)
```
와 같습니다.

---

> 이에 따라 반복문, 재귀문이 더 복잡해질수록 시간 복잡도가 기하급수적으로 늘어나는 것을 확인할 수 있습니다.
