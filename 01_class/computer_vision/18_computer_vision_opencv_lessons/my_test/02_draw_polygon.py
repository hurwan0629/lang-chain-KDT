import cv2
from pathlib import Path

IMG_DIR = Path() / ".." / "images"

img1 = IMG_DIR / "dog.bmp"

img1 = cv2.imread(img1)
img1_center_tuple = (round(img1.shape[1]/2), round(img1.shape[0]/2))
img1_short_side = min(img1.shape[0], img1.shape[1])

cv2.rectangle(img1, (50, 200), (100, 400), (255, 127, 127), 3)
cv2.circle(
    img1,
    img1_center_tuple, #(round(img1.shape[1]/2), round(img1.shape[0]/2)),
    round(min(img1.shape[0], img1.shape[1])/4),
    (0, 0, 0),
    3
)

cv2.putText(
    img1,
    "텍스트입니다",
    img1_center_tuple,# (round(img1.shape[1]/2)-200, round(img1.shape[0]/2)+100),
    cv2.FONT_HERSHEY_COMPLEX,
    1.0,
    (0, 0, 0),
    200
)

cv2.imshow("rectangle", img1)

cv2.waitKey(0)
cv2.destroyAllWindows()