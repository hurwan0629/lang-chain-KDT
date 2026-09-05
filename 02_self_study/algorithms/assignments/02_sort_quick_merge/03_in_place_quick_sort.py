# 공간 활용도 높은 퀵 정렬

import random
from typing import Literal
import math

# 중복 없이 값 추출
target_l = random.sample(range(1, 2001), k=random.randint(20, 30))
# target_1 = [i for i in range(1, 26)]

# 새로 수입한 문법 Literal..!
def quick_sort(target_l: list[int], order_type: Literal["asc", "desc"] = "asc") -> tuple[list[int], int]:

  count = 0
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
  # # # # # #  # # # #  pivot 정해서 리스트 나누기용 함수 # # # # # # # # # # # # # # # # # #
  def divide(start: int, end: int) -> int:
    nonlocal count

    pivot = target_l[end]
    i = start-1
    for j in range(start, end):
      count += 1
      # pivot을 기준으로 크고 작은 부분을 나누기 
      if target_l[j] < pivot if order_type == "asc" else target_l[j] > pivot:
        i += 1
        target_l[i], target_l[j] = target_l[j], target_l[i]

    # pivot을 중앙으로 보내주기
    target_l[i+1], target_l[end] = pivot, target_l[i+1]
    return i+1
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

  # 실행하기
  def sort(start: int, end: int):
    # 1칸이면 return
    if start >= end:
      return
    pivot_index = divide(start, end)
    
    sort(start, pivot_index-1)
    sort(pivot_index+1, end)

  sort(0, len(target_l)-1)

  return target_l, count


l = len(target_l)
print(f"길이: {l}")
print(f"[n log n](버림) = {l * (int(math.log2(l))) }")
print(target_l)
print("\n --- asc --- \n")
result = quick_sort(target_l, "asc")
print(f"결과: {result[0]}\n탐색 횟수: {result[1]}")
print("\n --- desc --- \n")
result = quick_sort(target_l, "desc")
print(f"결과: {result[0]}\n탐색 횟수: {result[1]}")
