import cv2
from pathlib import Path
import matplotlib.pyplot as plt

img = cv2.imread(str(Path() / ".." / "images" / "dog.bmp"))

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# cv2.imshow("gray", gray)

hist = cv2.calcHist(
    [img], # img = 색깔 이미지
    [0], # 그중에서 B 채널 이미지 선택
    None,   # None을 통해 사진의 모든 면적 추출
    [256],# hist bin의 개수
    [0, 256] # 값의 범위를 지정해줌
)

cdf = hist.cumsum()

print("cdf.shape", cdf.shape)

plt.figure(figsize=(4, 4))
plt.subplot(1, 1, 1)
plt.plot(cdf)
plt.tight_layout()
plt.show()


# print(hist.shape)
# plt.figure(3, figsize=(12, 4))
# plt.subplot(1, 3, 1)
# plt.plot(cv2.calcHist(
#     [img],
#     [0],
#     None,
#     [256],
#     [0, 256]
# ))
# plt.xlim([0, 256])
#
# plt.subplot(1, 3, 2)
# plt.plot(cv2.calcHist(
#     [img],
#     [1],
#     None,
#     [256],
#     [0, 256]
# ))
# plt.xlim([0, 256])
#
# plt.subplot(1, 3, 3)
# plt.plot(cv2.calcHist(
#     [img],
#     [2],
#     None,
#     [256],
#     [0, 256]
# ))
# plt.xlim([0, 256])
# plt.show()

equalized = cv2.equalizeHist(gray)

cv2.imshow("original", gray)
cv2.imshow("equalized", equalized)

cv2.waitKey(0)
cv2.destroyAllWindows()