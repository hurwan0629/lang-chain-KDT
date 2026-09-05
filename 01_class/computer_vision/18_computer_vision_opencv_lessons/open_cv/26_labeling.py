import cv2
import numpy as np

"""
Connected Components Labeling (연결요소 라벨링)
이진 영상에서 서로 붙어있는 흰색 픽셀 덩어리를 하나의 객체로 보고 번호를 붙이는 작업

이진화를 하는 이유로는 특별히 

"""

from pathlib import Path

img = cv2.imread(str(Path() / ".." / "images" / "keyboard.bmp"), cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread(str(Path() / ".." / "images" / "keyboard.bmp"), cv2.IMREAD_COLOR)

cv2.imshow("keyboard", img)

# 스레시홀드로 이진화
_, img_bin = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

dst = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

cv2.imshow("img", img)

# 내가 붙어있는 픽셀 덩어리에 대한 정보를 가져오는 메서드
# 라벨링을 수행하면서 객체에 대한 정보를 계산
# count: 전체 라벨 개수 (배경 포함)
# labels: 원본 영상과 크기가 같은 2차원 배열이며, 각각의 픽셀이 몇번 객체에 속하는지 저장
# status: 각 객체의 위치와 크기 정보. [left, top, width, height, area]
# centroids: 각 객체의 중심 좌표
count, labels, stats, centroids = cv2.connectedComponentsWithStats(img_bin, connectivity=8)
print("라벨 개수(배경 포함): ", count)
print("라벨 개수(배경 제외): ", count-1)
# cv2.connectedComponentsWithStats()

print("labels shape: ", labels.shape)
print("labels unique: ", np.unique(labels))
# print(np.where(lambda x: x==24, labels))
print("labels 일부: ", labels[:10, :10])

# stats에 객체의 위치와 크기중에서 area가 1이거나 width/height가 1일수록 노이즈일 확률이 높아진다.
print(f"stats: {len(stats)}")
# print(stats)

print(f"centroids: {len(centroids)}")
# print(centroids)

for i in range(1, count):
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    area = stats[i, cv2.CC_STAT_AREA]

    # 노이즈 제거
    if area < 30:
        continue

    cx, cy = centroids[i]

    cv2.rectangle(img_color, (x, y), (x+w, y+h), (0, 255, 255), 2)
    cv2.circle(img_color, (int(cx), int(cy)), 3, (0, 0, 255), -1)

    cv2.imshow("labeling", img_color)

cv2.imshow("bin", img_bin)

cv2.waitKey(0)
cv2.destroyAllWindows()


