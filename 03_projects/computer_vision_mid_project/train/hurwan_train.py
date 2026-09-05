import torch

"""
한빈님 카메라 기준 640 x 480 (W, H) 기본적으로 데이터는 다음과 같이 받는다고 가정

opencv: (H, C, W) 로 받음.

이를 Dataset, ToTensor을 이용하여 다음과 같은 방식으로 변환

(B, C, H, W)
"""

"""
train.py에서 작업하는 것들
- 손실함수
- 옵티마이저
- 스케줄러
- one_epoch
- validate()
- checkpoint save
"""
