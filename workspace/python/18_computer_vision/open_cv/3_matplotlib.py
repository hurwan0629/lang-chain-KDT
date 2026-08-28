import cv2
import matplotlib.pyplot as plt

img_gray = cv2.imread("./images/dog.bmp", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR)

"""
OpenCV의 RGB 색상 채널 순서: BGR
Matplotlib RGB 색상 채널 순서: RGB
"""

img_color_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)

plt.subplot(1, 2, 1)
plt.axis("off")
plt.title("Grayscale")
plt.imshow(img_gray, cmap="gray")

plt.subplot(1, 2, 2)
plt.axis("off")
plt.title("Color")
plt.imshow(img_color_rgb)

plt.tight_layout()
plt.show()