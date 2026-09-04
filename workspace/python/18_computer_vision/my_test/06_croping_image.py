"""
기본 점 및 박스 위치 등 설정하기
"""

DOT_RADIUS = 15
MARGIN = 5
LINE_WIDTH = 5

DST_H = 500
DST_W = round(DST_H * 297 / 210)

import cv2
from pathlib import Path
import numpy as np

# 이미지 가져오기
IMG = Path() / ".." / "images" / "namecard.jpg"

original_img = cv2.imread(str(IMG))


# 점들 그리기
h = original_img.shape[0]
w = original_img.shape[1]

print(f"h: {h} / w: {w}")

dot_pos = {
#   num: (h, w)
    1: (DOT_RADIUS+MARGIN, DOT_RADIUS+MARGIN),
    2: (DOT_RADIUS+MARGIN, w-DOT_RADIUS-MARGIN),
    3: (h-DOT_RADIUS-MARGIN, w-DOT_RADIUS-MARGIN),
    4: (h-DOT_RADIUS-MARGIN, DOT_RADIUS+MARGIN)
}

dst_quad = np.array([
    [0, 0],
    [DST_W - 1, 0],
    [DST_W, DST_H - 1],
    [0, DST_H - 1]
], dtype=np.float32)

src_quad = []

# 이미지 그려주는 함수
def draw():
    global original_img, dot_pos, src_quad
    img = original_img.copy()

    src_quad = []

    for dot_y, dot_x in dot_pos.values():

        # print(dot_y, dot_x)

        src_quad.append([dot_x, dot_y])

        cv2.circle(img, (dot_x, dot_y), DOT_RADIUS, (0, 255, 0), thickness=-1)

    # 이미지 그려내기
    cv2.imshow("original", img)

    src_quad = np.array(src_quad, dtype=np.float32)

    cv2.polylines(img, [src_quad.astype(np.int32)], True, (0, 0, 255), 3)

    cv2.imshow("original", img)

def crop():
    global src_quad, dst_quad

    perspective_matrix = cv2.getPerspectiveTransform(src_quad, dst_quad)

    dst = cv2.warpPerspective(original_img, perspective_matrix, (DST_W, DST_H))

    cv2.imshow("cropped", dst)

"""
마우스 상태 추적기 
"""

selected_dot = None
is_dragging = False

def on_mouse(event, x, y, flags, param):
    global selected_dot, is_dragging

    # 마우스가 클릭했을 때
    if event == cv2.EVENT_LBUTTONDOWN:

        # 점 4개중 하나의 위치 위에 마우스가 존재할 때
        for key, (dot_y, dot_x) in dot_pos.items():
            # 마우스와 점 중앙의 유클리드 거리
            dx = x - dot_x
            dy = y - dot_y

            distance = np.sqrt(dx**2 + dy**2)

            if distance < DOT_RADIUS:
                selected_dot = key
                is_dragging = True
                print("dot selected:", key)
                break

    # 마우스 우클릭을 땠을 때
    if event == cv2.EVENT_MOUSEMOVE and is_dragging:
        dot_pos[selected_dot] = (y, x)

        # 이미지 다시 그려주기
        draw()

    elif event == cv2.EVENT_LBUTTONUP and is_dragging:
        selected_dot=None
        is_dragging=False




draw()
cv2.setMouseCallback("original", on_mouse)

while True:
    if cv2.waitKey(0) & 0xFF == 32:
        crop()
    elif cv2.waitKey(0) & 0xFF == 27:
        cv2.waitKey(0)
        cv2.destroyAllWindows()


