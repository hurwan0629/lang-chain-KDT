# [머신러닝] ultralytics 라이브러리

`Ultralytics`는 YOLO를 쉽게 사용할 수 있게 만든 라이브러리 및 회사입니다.

파이썬 에서 이를 활용한다면 굉장히 간단하게 객체탐지 모델을 만들 수 있습니다.

```python
from ultralytics import YOLO

# 모델 끝
model = YOLO("yolo11s-seg.pt") 
```

이후에 위의 코드를 실행시키게 된다면 