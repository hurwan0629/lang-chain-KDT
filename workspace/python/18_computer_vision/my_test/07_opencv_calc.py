import cv2
import numpy as np
from pathlib import Path

IMG_PATH = Path("../images/airplane.bmp")

img = cv2.imread(str(IMG_PATH))

print(type(img))
print(img.shape)
print(img.dtype)


y_bins = np.linspace(0, img.shape[0], 3, dtype=int)
x_bins = np.linspace(0, img.shape[1], 3, dtype=int)

for y_idx in range(len(y_bins)-1):
    for x_idx in range(len(x_bins)-1):
        show_img = img[
                y_bins[y_idx]:y_bins[y_idx+1],
                x_bins[x_idx]:x_bins[x_idx+1]
            ].copy()
        # B
        # show_img[:, :, 0] = np.zeros(show_img.shape[:-1])
        # G
        # show_img[:, :, 1] = np.zeros(show_img.shape[:-1])
        # R
        # show_img[:, :, 2] = np.zeros(show_img.shape[:-1])
        cv2.imshow(
            f"({y_idx}, {x_idx})",
            show_img
        )

cv2.imshow("original", img)
cv2.waitKey(0)
cv2.destroyAllWindows()