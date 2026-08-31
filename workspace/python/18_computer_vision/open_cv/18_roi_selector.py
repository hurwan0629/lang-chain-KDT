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
        is_dragging = True
        start_x = x
        start_y = y

    elif event == cv2.EVENT_MOUSEMOVE and is_dragging:
        preview = img.copy()
        x1 = min(start_x, x)
        y1 = min(start_y, y)
        x2 = max(start_x, x)
        y2 = max(start_y, y)
        cv2.rectangle(preview, (x1, y1), (x2, y2), color, 2)
        cv2.imshow("img", preview)

IMG_DIR = Path() / ".." / "images"

img = cv2.imread(str(IMG_DIR / "sun.jpg"))

cv2.imshow("img", img)

cv2.setMouseCallback("img", on_mouse)

cv2.waitKey(0)
cv2.destroyAllWindows()