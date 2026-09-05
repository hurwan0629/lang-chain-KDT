import cv2
import numpy as np
from pathlib import Path

def draw_roi(image, corners):
    preview = image.copy()
    point_color = (192, 192, 255)
    line_color = (128, 128, 255)

    for pt in corners:
        cv2.circle(preview, tuple(pt.astype(int)), 12, point_color, -1)

    for i in range(4):
        pt1 = tuple(corners[i].astype(int))
        pt2 = tuple(corners[(i+1) % 4].astype(int))
        cv2.line(preview, pt1, pt2, line_color, 2)

    return preview


def on_mouse(event, x, y, flags, param):

    global src_quad, drag_src

    if event == cv2.EVENT_LBUTTONDOWN:
        for i in range(4):
            # 두 점 사이의 직선거리
            distance = cv2.norm(src_quad[i] - np.array([x, y], dtype=np.float32))
            if distance < 20:
                drag_src[i] = True
                break


    elif event == cv2.EVENT_MOUSEMOVE:
        for i in range(4):
            if drag_src[i]:
                # 좌표가 이미지 바깥으로 나가지 않도록 제한
                new_x = np.clip(x, 0, w - 1)
                new_y = np.clip(y, 0, h - 1)
                src_quad[i] = (new_x, new_y)
                preview = draw_roi(img, src_quad)
                cv2.imshow('img', preview)
                break

    elif event == cv2.EVENT_LBUTTONUP:
        drag_src = [False, False, False, False]



img = cv2.imread(str(Path() / ".." / "images" / "namecard.jpg"))

h, w = img.shape[:2]

dst_h = 500
dst_w = round(dst_h * 297 / 210)


# 왼쪽 위, 왼쪽 아래, 오른쪽 아래, 오른쪽 위
src_quad = np.array([
    [30, 30],
    [30, h - 30],
    [w - 30, h - 30],
    [w - 30, 30]
], dtype=np.float32)

dst_quad = np.array([
    [0, 0],
    [0, dst_h - 1],
    [dst_w - 1, dst_h - 1],
    [dst_w - 1, 0]
], dtype=np.float32)

drag_src = [False, False, False, False]



display = draw_roi(img, src_quad)

cv2.imshow('img', display)
cv2.setMouseCallback("img", on_mouse)

print('네 꼭짓점을 드래그하여 영역을 맞추세요.')
print('Enter: 투시 변환')
print('ESC: 종료')

while True:
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyAllWindows()
        raise SystemExit
    elif key in (10, 13):
        break

prespective_matrix = cv2.getPerspectiveTransform(src_quad, dst_quad)
dst = cv2.warpPerspective(img, prespective_matrix, (dst_w, dst_h), flags=cv2.INTER_CUBIC)
cv2.imshow("perspective result", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()