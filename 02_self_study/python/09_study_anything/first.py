from collections import Counter

# 클래스별 발견된 것들에 대한 dict들 클래스와 확신도
detections = [
  {"class": "bottle", "confidence": 0.92},
  {"class": "can", "confidence": 0.72},
  {"class": "bottle", "confidence": 0.65},
  {"class": "paper", "confidence": 0.42}
]

# 1. confidence가 0.5 이상인 탐지만 선택
# detection 순회하면서 확신도가 높은것들을 선택
filtered = [
  item for item in detections
  if item["confidence"] >= 0.5
]

# 2. confidence가 높은 순서로 정렬
# 필터링된 리스트에서 확신도 높은것들을 순서대로 정렬
sorted_items = sorted(
  filtered,
  key=lambda item: item["confidence"],
  reverse=True
)

# 카운터를 이용해서 클래스별 개수 정리하기.
counts = Counter(
  item["class"] for item in sorted_items
)

for name, count in counts.items():
  print(f"{name}: {count}")