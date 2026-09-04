import cv2
from pathlib import Path
import numpy as np

IMG_DIR = Path() / ".." / "images"

img = cv2.imread(str(IMG_DIR / "polygon.bmp"))

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("gray", img_gray)

img_rand = np.random.choice(
    [0, 255],
    (224, 224),
).astype(np.uint8)

print(img_rand.shape)
print(np.unique(img_rand))

img_rand_blur = cv2.blur(
    img_rand,
    (3, 3)
)
img_rand_blur = cv2.blur(
    img_rand_blur,
    (3, 3)
)
img_rand_blur = cv2.blur(
    img_rand_blur,
    (3, 3)
)

canny = cv2.Canny(
    img_rand_blur,
    100,
    200
)

cv2.imshow("rand", img_rand)
cv2.imshow("img_rand_blur", img_rand_blur)
cv2.imshow("canny", canny)

cv2.waitKey(0)
cv2.destroyAllWindows()