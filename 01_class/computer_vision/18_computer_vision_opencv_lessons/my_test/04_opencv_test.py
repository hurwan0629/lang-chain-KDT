import cv2
from pathlib import Path

import numpy as np

IMG_DIR = Path() / ".." / "images"

airplane_bgr = cv2.imread(
    str(IMG_DIR / "airplane.bmp"),
    cv2.IMREAD_COLOR_BGR
)

# # # # # # # # # # # # 축 그려보기 # # # # # # # # # # # #

print(airplane_bgr.shape)

airplane_hsv = cv2.cvtColor(airplane_bgr, cv2.COLOR_BGR2HSV)

print(airplane_hsv.shape)

airplane_gray = cv2.cvtColor(airplane_bgr, cv2.COLOR_BGR2GRAY)

print(airplane_gray.shape)

airplane_gray = np.expand_dims(airplane_gray, axis=-1)

print(airplane_gray.shape)

# # # # # # # # # # # # 이미지 출력해보기 # # # # # # # # # # # #

cv2.imshow("bgr", airplane_bgr)
cv2.waitKey(1)
cv2.destroyWindow("bgr")

cv2.imshow("gray", airplane_gray)
cv2.waitKey(1)
cv2.destroyWindow("gray")


airplane_gray2hsv = cv2.cvtColor(airplane_gray, cv2.COLOR_GRAY2BGR)
cv2.imshow("gray2hsv", airplane_gray2hsv)

cv2.waitKey(1)
cv2.destroyAllWindows()

print("gray2hsv.shape", airplane_gray2hsv.shape)
print("gray2hsv[0, 0]", airplane_gray2hsv[0, 0])

print()

# # # # # # # # # # # # 이미지 크롭 하기 # # # # # # # # # # # #

w = airplane_bgr.shape[1]
h = airplane_bgr.shape[0]

airplane_crop = airplane_bgr[h*1//4:h*3//4, w*1//4:w*3//4]

cv2.imshow("crop", airplane_crop)

cv2.waitKey(1)
cv2.destroyWindow("crop")

crop_hsv_lower = (0, 70, 70)
crop_hsv_upper = (17, 255, 255)

airplane_hsv_red_mask = cv2.inRange(airplane_hsv, crop_hsv_lower, crop_hsv_upper)

print(
    np.unique(airplane_hsv_red_mask)
)

cv2.imshow("airplane_hsv_red_mask", airplane_hsv_red_mask)

cv2.waitKey(1)
cv2.destroyAllWindows()

airplane_rgb_only_red_bool \
    = airplane_hsv_red_mask.astype(bool)

cv2.imshow("airplane_bgr", airplane_bgr)

cv2.imshow(
    "airplane_hsv_red_masked",
    np.expand_dims(airplane_hsv_red_mask, axis=-1) & airplane_bgr
       )

cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)

cv2.imshow("hsv", airplane_hsv)
cv2.waitKey(1)
cv2.destroyAllWindows()

kernel= np.ones((2, 2), dtype=np.uint8)

airplane_hsv_red_mask_erotion = cv2.erode(
    airplane_hsv_red_mask,
    kernel,
    iterations=1
)

airplane_hsv_red_mask_erotion_2 = cv2.erode(
    airplane_hsv_red_mask_erotion,
    kernel,
    iterations=1
)


cv2.imshow("before", airplane_hsv_red_mask)
cv2.imshow("erotion", airplane_hsv_red_mask_erotion)
cv2.imshow("erotion*2", airplane_hsv_red_mask_erotion_2)

airplane_hsv_red_mask_erotion_2_dilation = cv2.dilate(
    airplane_hsv_red_mask_erotion_2,
    kernel,
    iterations=1
)

cv2.imshow("erotion*2>dilation", airplane_hsv_red_mask_erotion_2_dilation)

cv2.waitKey(1)
cv2.destroyAllWindows()

print(np.unique(airplane_hsv_red_mask_erotion))

print("\n === bitwise === \n")

rand_arr_1 = np.round(
    np.random.rand(10, 10)
)

print("rand_arr_1.sum()", rand_arr_1.sum())

rand_arr_2 = np.round(
    np.random.rand(10, 10)
)

print("rand_arr_2.sum()", rand_arr_2.sum())

bit_and = cv2.bitwise_and(rand_arr_1, rand_arr_2)

print("type(bit_and):", type(bit_and))
print("bit_and.sum():", bit_and.sum())

print()

bit_or = cv2.bitwise_or(rand_arr_1, rand_arr_2)

print("type(bit_or):", type(bit_or))
print("bit_or.sum():", bit_or.sum())

print()

bit_xor = cv2.bitwise_xor(rand_arr_1, rand_arr_2)

print("type(bit_xor):", type(bit_xor))
print("bit_xor.sum():", bit_xor.sum())

bit_1_not_2 = cv2.bitwise_and(rand_arr_1, cv2.bitwise_not(rand_arr_2))

print("type(bit_1_not_2):", type(bit_1_not_2))
print("bit_1_not_2.sum():", bit_1_not_2.sum())

print()

bit_2_not_1 = cv2.bitwise_and(rand_arr_2, cv2.bitwise_not(rand_arr_1))

print("type(bit_2_not_1):", type(bit_2_not_1))
print("bit_2_not_1.sum():", bit_2_not_1.sum())

