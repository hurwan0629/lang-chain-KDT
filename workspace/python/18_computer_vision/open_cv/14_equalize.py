from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import sys

import numpy

print(Path().cwd())

IMG_DIR = Path() / ".." / "images"

if not IMG_DIR.exists():
    print("이미지 디렉토리가 존재하지 않습니다.")
    sys.exit(0)

print("이미지 디렉토리:", IMG_DIR.cwd(), end="\n")

img_gray = cv2.imread(str(IMG_DIR / "Hawkes.jpg"), cv2.IMREAD_GRAYSCALE)
img_color: numpy.ndarray = cv2.imread(str(IMG_DIR / "field.bmp"))

"""
색상 표현 방식: YCrCb 
- 컬러 이미지를 표현하는 또 다른 색 공간
- 밝기와 색상 정보를 분리해서 저장
- (Y = 밝기, Cr(붉은 성향)/Cb(푸른 성향) = 색상 정보)
"""
ycrcb = cv2.cvtColor(img_color, cv2.COLOR_BGR2YCrCb)
ycrcb[..., 0] = cv2.equalizeHist(ycrcb[..., 0])
equalized_color = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

if False:
    cv2.imshow("gray original", img_gray)
    cv2.imshow("color original", img_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# print("min:", img_gray.min())
# print("min:", img_gray.max())

"""
normalize 함수 = 표준화 해주는 함수 -> 평균을 구해서 편차로 만들어 준 뒤 
- 정규화
- 값의 범위 조정
- 최솟값/최댓값
- 기본적으로 비율을 유지하면서 변화
- 본래 대비개선이 주 목적은 아님
- 데이터 범위 통일 및 시각화, 전처리할 때 사용하는 함수.
"""

normalized_gray = cv2.normalize(img_gray, None, 0, 255, cv2.NORM_MINMAX)

"""
equalizeHist()
- 히스토그램 평활화 (히스토그램을 이용해서 평활화 시킨다)
- 대비 향상
- 픽섹을의 분포
- 일반적으로 0 ~ 255
- 대비 개선에 특화
- 픽셀의 분포가 80~150까지 있다면
"""

# 이미지가 아닌 히스토그램임
equalized_gray = cv2.equalizeHist(img_gray)

cv2.imshow("gray original", img_gray)
cv2.imshow("color original", img_color)
cv2.imshow("gray normalized", normalized_gray)
cv2.imshow("equalized_gray", equalized_gray)
cv2.imshow("color equalized", equalized_color)
# print(type(equalized_gray)) # <class 'numpy.ndarray'>

hist_original = cv2.calcHist([img_gray], [0], None, [256], [0, 256])
hist_equalized = cv2.calcHist([equalized_gray], [0], None, [256], [0, 256])
hist_normalized = cv2.calcHist([normalized_gray], [0], None, [256], [0, 256])

# plt.figure(figsize=(12, 4))
histograms = {
    "original": hist_original,
    "equalized": hist_equalized,
    "normalized": hist_normalized
}

# print(hist_equalized.shape) # (256, )

# print(type(hist_original)) # <class 'numpy.ndarray'>

for i, (title, hist) in enumerate(histograms.items(), start=1):
    plt.subplot(2, 3, i)
    plt.plot(hist)
    plt.title(title)
    plt.xlim([0, 256])

for i, (title, channel) in enumerate(zip(["B", "G", "R"], [0, 1, 2]), start=4):
    hist = cv2.calcHist(
        [img_color],
        [channel],
        None,
        [256],
        [0, 256]
    )
    plt.subplot(2, 3, i)
    plt.plot(hist)
    plt.title(title)
    plt.xlim([0, 256])

plt.tight_layout()
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()
