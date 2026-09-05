import random
from typing import Literal
import math

# 중복 없이 값 추출
target_l = random.sample(range(1, 2001), k=random.randint(20, 30))
# target_1 = [i for i in range(1, 26)]

# 새로 수입한 문법 Literal..!
def quick_sort(target_l: list[int], order_type: Literal["asc", "desc"] = "asc", count: int = 0) -> tuple[list[int], int]:
  # 0. 값이 하나이면 반환하기
  if len(target_l) <= 1:
    return target_l, 0
  # 1. 리스트에서 피벗 뽑기 (빠르게 맨 앞의 값)
  pivot = target_l[0]

  # pivot을 기준으로 리스트 나누기
  front: list[int] = []
  back: list[int] = []

  for v in target_l[1:]:
    count += 1
    if v < pivot if order_type == "asc" else v > pivot:
      front.append(v)
    else:
      back.append(v)
    
  # 다시 정렬해서 합치기
  f, add1 = quick_sort(front, order_type)
  b, add2 = quick_sort(back, order_type)

  return f + [pivot] + b, add1 + add2 + count

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
