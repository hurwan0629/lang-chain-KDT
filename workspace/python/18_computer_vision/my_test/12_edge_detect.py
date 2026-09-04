import cv2
from pathlib import Path
import matplotlib.pyplot as plt

img = cv2.imread(str(Path() / ".." / "images" / "man.jpg"))

img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 평활화 전 분포 확인
hist = cv2.calcHist(
    [img_gray],
    [0],
    None,
    [256],
    [0, 256]
)

# 평활화

img_gray_eq = cv2.equalizeHist(img_gray)

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(hist)

# 평활화 히스토그램 확인

new_hist = cv2.calcHist(
    [img_gray_eq],
    [0],
    None,
    [256],
    [0, 256]
)

plt.subplot(2, 1, 2)
plt.plot(new_hist)
plt.tight_layout()
plt.show()

# 이미지 차이 출력

cv2.waitKey(0)

plt.clf()
plt.close()
plt.figure(figsize=(16, 16))

img_list = []

img_list.append({"gray":img_gray})
cv2.imshow("gray", img_gray)

img_gray_canny = cv2.Canny(img_gray, 100, 200)
img_list.append({"img_gray_canny":img_gray_canny})
cv2.imshow("gray_canny", cv2.Canny(img_gray, 100, 200))

img_list.append({"img_gray_eq":img_gray_eq})
cv2.imshow("img_gray_eq", img_gray_eq)

img_gray_eq_canny = cv2.Canny(img_gray_eq, 100, 200)
img_list.append({"img_gray_eq_canny":img_gray_eq_canny})
cv2.imshow("img_gray_eq_canny", cv2.Canny(img_gray_eq, 100, 200))

# img_gray_eq에 평균 blur 걸어줘보기
img_gray_eq_blur = cv2.blur(
    img_gray_eq,
    (5, 5)
)
img_list.append({"img_gray_eq_blur": img_gray_eq_blur})


cv2.imshow("img_gray_eq_blur", img_gray_eq_blur)

img_gray_eq_blur_canny = cv2.Canny(img_gray_eq_blur, 100, 200)
img_list.append({"img_gray_eq_blur_canny": img_gray_eq_blur_canny})
cv2.imshow("img_gray_eq_blur_canny", cv2.Canny(img_gray_eq_blur, 100, 200))


# img_gray_eq에 gaussian_blur 걸어주기
img_gray_eq_gaussian = cv2.GaussianBlur(
    img_gray_eq,
    (5, 5),
    0
)

img_list.append({"img_gray_eq_gaussian": img_gray_eq_gaussian})

cv2.imshow("img_gray_eq_gaussian", img_gray_eq_gaussian)

img_gray_eq_gaussian_canny = cv2.Canny(img_gray_eq_gaussian, 100, 200)
img_list.append({"img_gray_eq_gaussian_canny": img_gray_eq_gaussian_canny})
cv2.imshow("img_gray_eq_gaussian_canny", img_gray_eq_gaussian_canny)

cv2.waitKey(0)
cv2.destroyAllWindows()