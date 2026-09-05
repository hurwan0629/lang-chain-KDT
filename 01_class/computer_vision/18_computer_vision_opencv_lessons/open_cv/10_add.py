import cv2
from pathlib import Path

"""
OpenCV의 산술 연산

이미지의 각 픽셀값에 일정 연산값을 더하거나 빼는 방식으로 밝기를 조절할 수 있음
"""

IMG_DIR = Path() / ".." / "images"

print("IMG_DIR:", IMG_DIR)

img_gray = cv2.imread(str(IMG_DIR / "dog.bmp"), cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread(str(IMG_DIR / "dog.bmp"), cv2.IMREAD_COLOR)

bright_gray = cv2.add(img_gray, 100)
bright_color = cv2.add(img_color, 100)
dark_gray = cv2.subtract(img_gray, 100)
multiply_gray = cv2.multiply(img_gray, 2)
divide_gray = cv2.divide(img_gray, 2)

cv2.imshow('gray', img_gray)
# cv2.imshow('color', img_color)
cv2.imshow('bright gray', bright_gray)
cv2.imshow('multiply_gray', multiply_gray)
cv2.imshow('divide_gray', divide_gray)
# cv2.imshow('bright color', bright_color)

cv2.waitKey(0)
cv2.destroyAllWindows()