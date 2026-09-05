import cv2
import math
from pathlib import Path

img = cv2.imread(
    str(Path() / ".." / "images" / "polygon.bmp"),
    cv2.IMREAD_GRAYSCALE
)

# 이진화
threshold, img_bin = cv2.threshold(
    img,
    0,
    255,
    cv2.THRESH_BINARY | cv2.THRESH_OTSU
)

print("img_bin threshold:", threshold)

cv2.imshow("img_bin", img_bin)

cv2.waitKey(0)
cv2.destroyAllWindows()

# 윤곽선 확인
contours, hierarchy = cv2.findContours(
    img_bin,
    cv2.RETR_CCOMP,
    cv2.CHAIN_APPROX_NONE
)

for i, contour in enumerate(contours):

    # 노드 개수를 출력하기
    print("contours node count:", len(contour))
    print(contour.shape)

    # 두 점 사이의 각도가 160도보다 크면 꼭짓점 +1 해주기
    angle_count = 0

    for i in range(len(contour)):

        # 순회하면서 contour 점에 대한 각도를 구해주기
        prev_node = contour[-1 if i == 0 else i][0]
        curr_node = contour[i][0]
        next_node = contour[0 if i == len(contour[i][0]) - 1 else i][0]

        # curr-prev 기울기
        prev_grad = (
            (prev_node[0] - curr_node[0])
            / (prev_node[1] - curr_node[1])
        )

        # curr-next 기울기
        next_grad = (
            (next_node[0] - curr_node[0])
            / (next_node[1] - curr_node[1])
        )

        # 각도 구하기
        # tan(k) = (prev_grad + next_grad) / (1 - prev_grad * next_grad)

        # 90도라면 패스해주기
        if prev_grad * next_grad == 1:
            continue

        tan_k = (
            (prev_grad + next_grad)
            / (1 - prev_grad * next_grad)
        )

        angle = math.atan(tan_k)

        # print(angle)

        if 200 > angle > 160:
            continue

        angle_count += 1

    print(angle_count)