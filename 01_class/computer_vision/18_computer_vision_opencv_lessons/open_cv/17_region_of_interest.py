"""
ROI (Region of Interest)
이미지 전체가 아닌 특정 관심 영역만 선택해서 처리
"""

import cv2
from pathlib import Path

IMG_DIR = Path() / ".." / "images"

img = cv2.imread(str(IMG_DIR / "sun.jpg"))

x = 182
y = 17
w = 120
h = 120

roi = img[y:y+h, x:x+w]
roi_copy = roi.copy()

img[y: y+h, x+w:x+2*w] = roi_copy

# print(img)
#            ndarray / 한쪽 꼭젓점(x, y), 한쪽 꼭짓점: (x, y) / (b, g, r), 두께
# 나중에 객체탐지에서 우리가 그리게 될 객체형태
# cv2.rectangle(img, (50, 200), (200, 300), (255, 0, 0), 3)

cv2.rectangle(img, (x, y), (x+2*w, y+h), (255, 0, 0), 3)

cv2.imshow("original", img)
cv2.imshow("ROI result", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()