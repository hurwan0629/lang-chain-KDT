import cv2
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread(str(Path() / ".." / "data" / "custom_images" / "001300.jpg"))

# [ 색상공간 변환하기 ]
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# [ 히스토그램 변환하기 ]
hist = cv2.calcHist([img], [0], None, [256], [0, 256])

img = cv2.equalizeHist(img)

hist_eq = cv2.calcHist([img], [0], None, [256], [0, 256])

# _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

# plt.plot(hist)
# plt.show()

# img = cv2.GaussianBlur(img, (3, 3), 0)
# img = cv2.GaussianBlur(img, (3, 3), 0)
# img = cv2.GaussianBlur(img, (3, 3), 0)
# img = cv2.GaussianBlur(img, (3, 3), 0)

# canny
# img = cv2.Canny(img, 100, 200)

# [connectedComponents]
num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img, connectivity=8)
# print(type(labels))
# print(labels.shape)
# print(stats[0])
print(num_labels)
print(stats.shape)
print(centroids.shape)

result = np.zeros_like(img)
for i in range(1, num_labels):
    area = stats[i, cv2.CC_STAT_AREA]

    if area > 1000:
        result[labels == i] = 255

cv2.imshow("hourse", result)

cv2.waitKey(0)
cv2.destroyAllWindows()