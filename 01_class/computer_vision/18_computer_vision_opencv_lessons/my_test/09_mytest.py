import cv2
from pathlib import Path
import numpy as np

img = cv2.imread(Path("../images/dog.bmp"))

Y_MAX = img.shape[0]
X_MAX = img.shape[1]

def onmouse(event, x, y, flag, param):

    global img

    PEN_THICKNESS = 3

    if event == cv2.EVENT_MOUSEMOVE:
        print("mouse move")

        y1 = min(y-PEN_THICKNESS, Y_MAX)
        y2 = max(y+PEN_THICKNESS, 0)
        x1 = min(x-PEN_THICKNESS, X_MAX)
        x2 = max(x+PEN_THICKNESS, 0)

        img[y1:y2, x1:x2] = np.full((y2-y1, x2-x1, 3), np.array([255, 255, 255], dtype=np.uint8))
        cv2.imshow("dog_rec", img)


# 1. 이미지
# 2. 좌상단
# 3. 우상단
# 4. RGB
# 5. thickness
cv2.rectangle(img, (50, 50), (200, 150), (0, 255, 0), 3)

cv2.imshow("dog_rec", img)

cv2.setMouseCallback("dog_rec", onmouse)

cv2.waitKey(0)
cv2.destroyAllWindows()