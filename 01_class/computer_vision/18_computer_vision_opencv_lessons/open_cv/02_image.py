"""
cv2.imread()를 이용하여 이미지 파일을 읽을 수 있습니다.

opencv로 읽어오면 Numpy 배열 형태로 읽어오는 함수

.imread() 안에는 어떤 방식으로 읽어올지에 대한 인자를 줄 수 있음.

cv.IMREAD_GRAYSCALE
- 이미지를 gray_scale로 읽어오게 됨.
- 배열의 형태는 (높이, 너비) (H, W) 순서로 가져오게 됨

cv2.IMREAD_COLOR
- 이미지를 컬러로 읽어옴
- 배열의 형태는 (H, W, C=3) (높이, 너비, 채널=3)가 됨
- OpenCV의 컬러 채널 순서는 [B, G, R]임
"""

import cv2
from pathlib import Path
import matplotlib.pyplot as plt

# bmp는 그림을 기본으로 저장할 수 있는 비트맵 형식의 이미지로 압축이 전혀 되지 않음
img_gray = cv2.imread((Path() / "../images/dog.bmp"), cv2.IMREAD_GRAYSCALE)
# jpeg는 이미지 용량을 압축해놓은 알고리즘이 들아간 포멧
img_color = cv2.imread((Path() /"../images/dog.jpg"), cv2.IMREAD_COLOR) # cv2.IMREAD_COLOR 생략 가능

print("그레이스케일 이미지 배열: ")
print(img_gray)

print("컬러 이미지 배열: ")
print(img_color)

cv2.imshow("gray", img_gray)
cv2.imshow("show image", img_color)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

"""
OpenCV의 RGB 색상 채널 순서: BGR
Matplotlib RGB 색상 채널 순서: RGB
"""

img_color_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)

plt.subplot(1, 2, 1)
# 격자 지우기
plt.axis("off")
plt.title("GrayScale")
plt.imshow(img_gray, cmap="gray")

print("컬러 이미지 배열: ")
print(img_color)

plt.subplot(1, 2, 2)
# 격자 지우기
plt.axis("off")
plt.title("Color")
plt.imshow(img_color_rgb)

plt.tight_layout()
plt.show()