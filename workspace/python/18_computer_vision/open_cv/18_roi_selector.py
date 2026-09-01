import cv2
from pathlib import Path

start_x = 0
start_y = 0
is_dragging = False
color = (255, 0, 0)

def on_mouse(event, x, y, flags, param):
    """마우스 드래깅을 이용해 ROI 따주기"""
    global start_x, start_y, is_dragging

    if event == cv2.EVENT_LBUTTONDOWN:
        """마우스 좌클릭 하면 드래깅 하고있다고 전역 처리하기"""
        is_dragging = True
        start_x = x
        start_y = y

    elif event == cv2.EVENT_MOUSEMOVE and is_dragging:
        """드래깅 플래그가 켜져있을 때 움직이면 실시간으로 움직여주기"""
        preview = img.copy()
        x1 = min(start_x, x)
        y1 = min(start_y, y)
        x2 = max(start_x, x)
        y2 = max(start_y, y)
        cv2.rectangle(preview, (x1, y1), (x2, y2), color, 2)
        cv2.imshow("img", preview)

    elif event == cv2.EVENT_LBUTTONUP and is_dragging:
        """드래그 플래그가 켜져있을 때 좌클릭을 뗀다면 그 크기를 잡고"""
        is_dragging = False
        x1 = min(start_x, x)
        y1 = min(start_y, y)
        x2 = max(start_x, x)
        y2 = max(start_y, y)

        w = x2 - x1
        h = y2 - y1

        if w <=0 or h <= 0:
            """마우스가 움직이지 않았다면 취소시켜주기"""
            cv2.imshow("img", img)
            print("영역이 설정되지 않았습니다.")

            return
        # 마우스로 구한 영역을 슬라이싱하기
        roi = img[y1:y2, x1:x2]
        selected = img.copy()
        cv2.rectangle(selected, (x1, y1), (x2, y2), color, 2)
        cv2.imshow("img", selected)
        cv2.imshow("roi", roi)

        print(f"ROI 위치: x={x1}, y={y1}, w={w}, h={h}")

IMG_DIR = Path() / ".." / "images"

img = cv2.imread(str(IMG_DIR / "sun.jpg"))

cv2.imshow("img", img)

cv2.setMouseCallback("img", on_mouse)

cv2.waitKey(0)
cv2.destroyAllWindows()