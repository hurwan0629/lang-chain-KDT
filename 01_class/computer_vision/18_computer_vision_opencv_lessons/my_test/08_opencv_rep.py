import cv2
import numpy as np

img = cv2.imread("../images/dog.bmp", cv2.IMREAD_COLOR)

# cv2.imshow("dog", img)

img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# cv2.imshow("dog_hsv", img_hsv)

y = np.linspace(0, img.shape[0], 4).astype(int)
x = np.linspace(0, img.shape[1], 4).astype(int)

mask = np.zeros(img.shape[:-1], dtype=np.uint8)
print(mask.shape)
print(x)
print(y)
mask[y[1]:y[2], x[1]:x[2]] = 255

result = cv2.copyTo(img, mask, img_hsv)

cv2.imshow("center masked", result)


cv2.waitKey(0)
cv2.destroyAllWindows()

