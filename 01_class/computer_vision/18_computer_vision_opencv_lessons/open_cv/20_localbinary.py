import cv2
import numpy as np
from pathlib import Path

IMG_DIR = Path() / ".." / "images"

img = cv2.imread(IMG_DIR / "sudoku.jpg", cv2.IMREAD_GRAYSCALE)

print(img.shape)

otsu_threshold, global_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

print("otsu_threshold:", otsu_threshold)

cv2.imshow("original", img)
cv2.imshow("global_otsu", global_otsu)


h = img.shape[0]
w = img.shape[1]

div = 4

div_img = img.copy()
for i in range(div):
    for j in range(div):
        x1 = (w * j)//4
        x2 = (w * (j+1))//4
        y1 = (h * i)//4
        y2 = (h * (i+1))//4

        # cv2.imshow("global_otsu", div_img[y1:y2, x1:x2])

        # cv2.waitKey(0)

        otsu_threshold, div_img[y1:y2, x1:x2] = cv2.threshold(div_img[y1:y2, x1:x2], 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        print(f"({y1:3d} ~ {y2:3d}, {x1:3d} ~ {x2:3d}): {otsu_threshold}", end="\t")

    print()

# cv2.imshow("div_img", div_img)

# 적응형 이진화
# adaptiveThreshold(): 픽셀마다 주변 영역을 보고 임계값을 계산
# adaptiveThreshold(img, maxValue, blockSize, C)
# adaptiveThreshold(img, maxValue, blockSize, C)
# maxValue: 조건을 만족한 픽셀에 넣을 값, blockSize: 주변 영역의 크기. 반드시 3 이상의 홀수, C: 계산된 주변 기존값에서 빼는 상수
# T= 주변 평균(또는 가중 평균) - C
# C가 커지면 임계값 T가 낮아지므로 같은 영상에서는 흰색으로 판정되는 픽셀이 더 많아질 수 있음
block_size = 9
C = 5
# 주변 픽셀의 단순 평균을 기준으로 사용하는 이진화
adaptive_mean = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, C)

cv2.imshow("adaptive_mean", adaptive_mean)

# 주변 픽셀에 Gaussian 가중치를 적용한 평균을 기준으로 사용
adaptive_gaussian = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, C)

cv2.imshow("adaptive_gaussian", adaptive_gaussian)

cv2.waitKey(0)
cv2.destroyAllWindows()