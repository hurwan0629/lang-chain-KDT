"""
HSV
색을 사람이 느끼는 방식에 조금 더 가깝게 표현하는 색 공간


H: 무슨 색 - 각도를 이용하여 표현 (0 ~ 179 정도까지 사용하는 경우가 많음)
S: 얼마나 선명한 색 - 채도를 이용 (0=투명, 커질수록 진해지는 형태) (0 ~ 255) Saturation - 선명도
V: 얼마나 밝은가 - 명도를 나타냄 (0 ~ 255)

H 범위 (색상 범위)
빨강:      0 ~
노랑: 약  30 ~
초록: 약  60 ~
청록: 약  90 ~
파랑: 약 120 ~
보라: 약 150 ~
"""

from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import sys
import numpy as np

print(Path().cwd())

IMG_DIR = Path() / ".." / "images"

if not IMG_DIR.exists():
    print("이미지 디렉토리가 존재하지 않습니다.")
    sys.exit(0)

print("이미지 디렉토리:", IMG_DIR.cwd(), end="\n")

img_color: np.ndarray = cv2.imread(str(IMG_DIR / "candies.png"))
airplane = cv2.imread(str(IMG_DIR / "airplane.bmp"))
field = cv2.imread(str(IMG_DIR / "field.bmp"))
mask = cv2.imread(str(IMG_DIR / "mask_plane.bmp"))

# print(img_color is None)
img_hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)


print(img_hsv.shape)

# 파란색에 해당하는 HSV 범위를 지정
# 실제 영상에서는 조명과 카메라에 따라 범위를 적절하게 조정
lower_blue = (90, 150, 0)
upper_blue = (150, 255, 255)

# cv2.inRange를 이용하여 첫번째 인자의 ndarray에서 두 범위안에 있는 픽셀만 뽑아줌 (bool 마스크)
blue_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)

airplane_only = cv2.copyTo(airplane, mask=mask)
composite = field.copy()
cv2.copyTo(airplane, mask, composite)

# print("blue mask")
# print(type(blue_mask))
# print(blue_mask.shape)
# print(np.unique(blue_mask.astype(bool)))

# cv2.imshow("original", img_color)
# cv2.imshow("blue mask", blue_mask)
# cv2.imshow("blue masked", cv2.bitwise_and(img_color, img_color, mask=blue_mask))
cv2.imshow("composite", composite)

cv2.waitKey(0)
cv2.destroyAllWindows()