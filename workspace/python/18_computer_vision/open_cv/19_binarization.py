import cv2
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

IMG_DIR = Path() / ".." / "images"

"""
이진화
픽셀 값을 두 그룹으로 나누는 영상 처리 기법

일반적인 8비트 이진 영상 > 검정 (0), 흰색(255)

# OCR(Optical Character Recognition) 광학 문자 인식
이미지에서 글자나 외곽선을 따는 방법
글꼴마다 성능이 달라질 수 있기때문에 추출하는게 어색할 수 있음

OCR, 문서 스캔, 윤곽선 검출, 객체 분리 등의 전처리에서 자주 사용됨
"""

img = cv2.imread(str(IMG_DIR / "cells.png"), cv2.IMREAD_GRAYSCALE)

hist = cv2.calcHist([img], [0], None, [256], [0, 256])

# (내가 지정한 thresh, ndarray)
threshold1, dst1 = cv2.threshold(
    img,
    100, # 임계값 기준 반환값의 [0] 인자
    255,
    cv2.THRESH_BINARY # 픽셀값이 > threshold 이면 maxvalue를 넣어줘라 & 작거나 같으면 0으로 만들어라
)
print("임계값 1:", threshold1)

threshold2, dst2 = cv2.threshold(
    img,
    210, # 임계값 기준 반환값의 [0] 인자
    255,
    cv2.THRESH_BINARY # 픽셀값이 > threshold 이면 maxvalue를 넣어줘라 & 작거나 같으면 0으로 만들어라
)
print("임계값 2:", threshold2)


"""
Otsu 자동 임계값
> THRESH_OTSU를 사용하면 임계값을 사람이 직접 정하지 않고 영상의 히스토그램을 이용해서 opencv가 임계값을 자동으로 선택
"""

otsu_threshold, dst_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

print("otsu_threshold:", otsu_threshold)



print(type(hist))

cv2.imshow("original", img)
cv2.imshow("threshold 100", dst1)
cv2.imshow("threshold 210", dst2)
cv2.imshow("threshold otsu", dst_otsu)


# # # # # # # # # # # # [ DELATE & ERODE ] # # # # # # # # # # # #
# kernel = np.ones((3, 3), dtype=np.uint8)
# dst2 = cv2.dilate(dst1, kernel, iterations=1)
# dst2 = cv2.dilate(dst2, kernel, iterations=1)
# dst2 = cv2.erode(dst2, kernel, iterations=1)
# dst2 = cv2.erode(dst2, kernel, iterations=1)
#
# cv2.imshow("threshold 100 > dilate > erode", dst2)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

cv2.waitKey(0)
cv2.destroyAllWindows()

# plt.plot(hist)
# plt.title("Grayscale Hisogram")
# plt.xlabel("Pixel Value")
# plt.ylabel("Count")
# plt.xlim([0, 256])
# plt.show()