from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import sys

IMG_DIR = Path() / ".." / "images"

if not IMG_DIR.exists():
    print("이미지 디렉토리가 존재하지 않습니다.")
    sys.exit(0)
print("이미지 디렉토리:", IMG_DIR.cwd(), end="\n")

img_gray = cv2.imread(str(IMG_DIR / "candies.png"), cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread(str(IMG_DIR / "CANDIES.png"))

"""
히스토그램
- 이미지 히스토그램은 픽셀값의 분포를 나타냄
- 그레이스케일 영상: 0(검정색) ~ 255(흰색) 의 분포
- 컬러 영상: B, G, R 각 채널별로 값의 분포
"""

# [img_gray]: 분석할 이미지 목록
# [0]: 분석할 채널 번호
# None: 특정 영역만 분석할 때 사용
# [256]: histSize. 구간(bin)의 개수
# [0, 256]: 분석할 값의 범위
hist_gray = cv2.calcHist([img_gray], [0], None, [256], [0, 256])


plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.plot(hist_gray)
plt.title("Grayscale Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Count")
plt.xlim([0, 256])


plt.subplot(1, 2, 2)
channel_indices = [0, 1, 2]
channel_names = ["B", "G", "R"]

for channel_index, channel_name in zip(channel_indices, channel_names):
    hist = cv2.calcHist([img_color], [channel_index], None, [256], [0, 256])
    plt.plot(hist, label=channel_name)

plt.title("BRG Channels Histogram")
plt.xlabel("Pixel Value")
plt.ylabel("Count")
plt.xlim([0, 256])

plt.legend()
plt.tight_layout()
plt.show()

# 채널을 b, g, r 채널로 나누어주기
b, g, r = cv2.split(img_color)
cv2.imshow("original", img_color)
cv2.imshow("B channel", b)

cv2.waitKey(0)
cv2.destroyAllWindows()

