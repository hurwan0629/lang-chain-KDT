import cv2
import numpy as np

img_gray = cv2.imread("./images/dog.bmp", cv2.IMREAD_GRAYSCALE)
img_color = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR)
img_original = cv2.imread("./images/dog.bmp", cv2.IMREAD_COLOR)

print("img_gray type:", type(img_gray))
print("img_gray shape:", img_gray.shape)    # (364, 548)
print("img_gray dtype:", img_gray.dtype)
# print("img_color type:", type(img_color))
print()
print("img_color type:", type(img_color))
print("img_color shape:", img_color.shape)  # (364, 548, 3)
print("img_color dtype:", img_color.dtype)

print()
h, w = img_color.shape[:2]
print(f"이미지 크기: {w} * {h}")

print("img_gray.ndim:", img_gray.ndim)

if img_color.ndim == 3:
    print("img_color는 Color 이미지입니다.")
elif img_color.ndim == 2:
    print("img_color는 GrayScale 이미지입니다.")


img1 = np.zeros((240, 500, 3), dtype=np.uint8) # 가로 320, 세로 240, 컬러(검은색)
# np.empty(): 메모리 공간만 할당하고 예측할 수 없는 값을 저장함
img2 = np.empty((240, 320), dtype=np.uint8)
img3 = np.full((240, 320), 240, dtype=np.uint8)
img4 = np.full((240, 320, 3), (255, 102, 255), dtype=np.uint8)
print(img4)

# cv2.imshow("original", img_color)

# print((img_color +  np.full(img_color.shape, (255, 102, 255), dtype=np.uint8)).max(axis=2))
# print(((img_color +  np.full(img_color.shape, (255, 102, 255), dtype=np.uint8)/3)/2).max())

"""
height, width = img_color.shape[:2]

for y in range(height):
    for x in range(width):
        img_color[y, x] = (255, 102, 255)
"""

img_color[:, :] = (255, 102, 255)

img_color_pink = ((img_color +  np.full(img_color.shape, (255, 102, 255), dtype=np.uint8))).round(0)
# print(img_color_pink)

cv2.imshow("originial", img_original)
cv2.imshow("original_pink", img_color_pink)
# cv2.imshow("zeros", img1)
# cv2.imshow("empty", img2)
# cv2.imshow("full_240", img3)
# cv2.imshow("deeppink", img4)

while True:
    key = cv2.waitKey(0)
    # ord는 아스키코드 값을 반환
    if key in (ord("i"), ord("I")):
        # uint8 이미지에서 각 픽셀에 대해 255를 뺀 값과 같음
        img_original = ~img_original
        cv2.imshow("original", img_original)
    elif key == 27: # ESC == 27 아스키코드
        break

cv2.waitKey(0)
cv2.destroyAllWindows()