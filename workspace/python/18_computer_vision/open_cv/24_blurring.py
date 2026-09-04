import cv2
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

IMG_DIR = Path() / ".." / "images"

# img = cv2.imread(str(IMG_DIR / "dog.bmp"))
# img = cv2.imread(str(IMG_DIR / "gaussian_noise.jpg"))
img = cv2.imread(str(IMG_DIR / "noise.bmp"))

"""
블러링

픽셀 주변의 픽셀들을 같이 보고 새로운 픽셀 값을 결정하는 것
"""

img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# 1. 평균 블러
# 현재 픽셀 주변의 값을 모두 더한 다음 평균을 구함 (빠르고 단순)
#   (예: 7*7)
# cv2.blur(입력 이미지, 커널 크기, 결과 저장할 배열, 커널의 기준점=None, 이미지 가장자리 처리 방법 상수)
# 이것을 가장 안쓰는 이유는 블러링을 쓰는 경우에는 **중요 경계**를 뽑기 위해 사용하지는 않기 때문에 객체탐지에서는 잘 사용하지 않는다.
# 중요한 경계와 노이즈를 구별하지 않음
# Mean Blur보다 Gaussian Blur를 더 많이 사용하는 편
#   중앙에 가장 큰 가중치를 주고, 중앙에서 멀어질수록 가중치를 작게 만드는 방식
mean_blur = cv2.blur(img, (23, 23))

# 2. Biliteral Filter
#   공간적으로 가까운지, 픽셀 세상/밝기가 비슷한지를 확인
#   배경과 객체를 비교할 때 경계의 면에서 픽셀 값이 크게 달라지게 됨
#   가까운데 색이 비슷: 많이 반영, 가깝지만 색이 매우다르면 적게 반영
#   이를 이용하여 테두리를 더 부각시키는 필터라고 볼 수 있습니다.
# cv2.bilateralFilter(이미지, 지름, 시그마컬러(픽셀값 또는 색상차이 허용), 시그마 스페이스)
#
# 시그마 컬러: 픽셀값 또는 색상 차이를 얼마나 허용할지 결정
#     (예: 값을 적게줌 > 색상이 조금만 달라도 다른 영역이라고 판단)
# 시그마 스페이스: 공간적으로 얼마나 떨어진 픽셀까지 영향을 줄지 결정
#   (예: 값을 크게 줌 > 더 멀리 있느 픽셀까지 고려할 수 있음)
#
# 단점: 테두리 계산까지 모두 하하여 속도가 느릴 수 있음
biliteral = cv2.bilateralFilter(img, 25, 100, 100)

# 3. Canny Edge Detection
# Edge: 픽셀 값이 급격하게 변하는 위치
# 컬러 이미지를 그레이스케일로 변환 > 밝기가 갑자기 변화하는 위치를 찾음
# lower - 임계값 자동 계산
# upper - 임계값 자동 계산
# 이미지 밝기의 중앙값을 기준으로 threshold를 정하는 휴리스틱(경험적 방법)을 통해서
# Canny threshold를 조절하거나 다른 방법으로 threshold를 결정하는 경우가 많음 (lower, upper)

# cv2.Canny(이미지, 낮음 임계값, 높은 임계값, 시그마X)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
median_value = np.median(gray)
lower = int(max(0, 0.7 * median_value))
upper = int(min(255, 1.3 * median_value))

print("Canny lower threshold:", lower)
print("Canny upper threshold:", upper)

# Canny 전에 가볍게 Gaussian Blur을 적용해 잡음 영향을 줄임
# edge_input = cv2.GaussianBlur(gray, (3, 3), 0)
edge_input = cv2.medianBlur(gray, 3, 0)
# edge_input = cv2.GaussianBlur(edge_input, (3, 3), 0)
# edge_input = cv2.GaussianBlur(edge_input, (3, 3), 0)
# edge_input = cv2.GaussianBlur(edge_input, (3, 3), 0)

canny_edge = cv2.Canny(
    edge_input, lower, upper, 3
)

# 4. 직접 평균 커널 만들기
# filter2D()을 사용하면 사용자가 직접 만든 커널을 적용할 수 있음
plt.figure(figsize=(10, 5))
for i, k in enumerate([5, 7, 9]):
    kernel = np.ones((k, k), dtype=np.float32) / (k*k)
    # -1: 출력 영상의 데이터 타입을 입력 영상과 같게 유지
    filtered = cv2.filter2D(img_rgb, -1, kernel)

    plt.subplot(1, 3, i+1)
    plt.imshow(filtered)
    plt.title(f"kernel size: {k} x {k}")
    plt.axis("off")

plt.tight_layout()
plt.show()

cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("original", img)
cv2.imshow("mean blur", mean_blur)
cv2.imshow("bilateral", biliteral)
cv2.imshow("edge_input", edge_input)
cv2.imshow("canny_edge", canny_edge)

cv2.waitKey(0)
cv2.destroyAllWindows()