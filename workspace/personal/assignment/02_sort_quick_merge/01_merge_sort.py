import random

from typing import Literal

import math

target_l = random.sample(range(1, 2001), k=random.randint(20, 30))

def merge_sort(l: list[int], order_type: Literal["asc", "desc"] = "asc", count: int = 0) -> tuple[list[int], int]:
  # # # # 그냥 먼저 다 len == 1이 될 때까지 쪼개버리기 (후위 처리) # # # # 
  if len(l) <= 1:
    return l, 0
  
  left, add1 = merge_sort(l[0:len(l)//2], order_type, count)
  right, add2 = merge_sort(l[len(l)//2:], order_type, count)

  # 성능 측정용 count 추가
  count += add1 + add2
  # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

  # 병합 준비하기
  # 왼쪽 리스트와 오른쪽 리스트에서 포인터(인덱스) 1씩 증가시키면서 합치기
  merged_l = []
  l_index = 0
  r_index = 0

  # 하나라도 끝까지 가면 끝내고 나머지 뒤에 붙이기
  while l_index < len(left) and r_index < len(right):
    count += 1
    # order_type에 따라 추가 조건 바꿔주기
    if left[l_index] <= right[r_index] if order_type == "asc" else left[l_index] > right[r_index]:
        merged_l.append(left[l_index])
        l_index += 1
    else:
        merged_l.append(right[r_index])
        r_index += 1

  merged_l += left[l_index:]
  merged_l += right[r_index:]

  return merged_l, count


l = len(target_l)
print(f"길이: {l}")
print(f"[n log n](버림) = {l * (int(math.log2(l))) }")
print(target_l)
print("\n --- asc --- \n")
result = merge_sort(target_l, "asc")
print(f"결과: {result[0]}\n탐색 횟수: {result[1]}")
print("\n --- desc --- \n")
result = merge_sort(target_l, "desc")
print(f"결과: {result[0]}\n탐색 횟수: {result[1]}")
