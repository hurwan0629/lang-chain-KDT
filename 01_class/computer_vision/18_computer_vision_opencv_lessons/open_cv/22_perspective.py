import cv2
import numpy as np
from pathlib import Path
"""
투시 변환 (Perspective Transform)
원근감 때문에 기울어져보이는 사각형 영역을 정면에서 바라본 것처럼 펴는데 사용

- 문서 스캔, 명암 보정, 책 페이지 보정 등
"""

IMG_DIR = Path() / ".." / "images"

img = cv2.imread(IMG_DIR / "pic.jpg")

dst_w = 800
dst_h = 600

src_quad = np.array([
    [371, 172],
    [1228, 158],
    [1421, 843],
    [209, 852]
], dtype=np.float32)

dst_quad = np.array([
    [0, 0],
    [dst_w - 1, 0],
    [dst_w, dst_h - 1],
    [0, dst_h - 1]
], dtype=np.float32)

perspective_matrix = cv2.getPerspectiveTransform(src_quad, dst_quad)
print(perspective_matrix)

dst = cv2.warpPerspective(img, perspective_matrix, (dst_w, dst_h))

preview = img.copy()
for pt in src_quad.astype(int):
    cv2.circle(preview, tuple(pt), 8, (0, 0, 255), -1)

cv2.polylines(preview, [src_quad.astype(np.int32)], True, (0, 255, 0), 3)

cv2.imshow("preview", preview)
cv2.imshow("source", img)
cv2.imshow("perspective result", dst)
cv2.waitKey(0)
cv2.destroyAllWindows()
