from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import sys

IMG_DIR = Path() / ".." / "images"

if not IMG_DIR.exists():
    print("이미지 디렉토리가 존재하지 않습니다.")
    sys.exit(0)
print("이미지 디렉토리:", IMG_DIR.cwd(), end="\n")

img1 = cv2.imread(str(IMG_DIR / "dog.jpg"))
img2 = cv2.imread(str(IMG_DIR / "square.bmp"))

# 1. 단순 덧셈. 255보다 큰 값은 255로 제한
dst_add = cv2.add(img1, img2)

# 2. 가중치 합성
# img1 * 0.5 + img2 * 0.5 + ?
dst_blend = cv2.addWeighted(img1, 0.2, img2, 0.5, 1)

# 3. 뺄셈. 음수가 되는 값은 0으로 제한
dst_subtract = cv2.subtract(img1, img2)

# 4. 절대 차이
# | img1 - img2 |
# 두 영상에서 픽셀값이 얼마나 다른지 확인할 때 사용
dst_absdiff = cv2.absdiff(img1, img2)

images = {
    "dst_add": dst_add,
    "dst_blend": dst_blend,
    "dst_subtract": dst_subtract,
    "dst_absdiff": dst_absdiff,
}


plt.figure(figsize=(10, 8))

for i, (title, image) in enumerate(images.items(), start=1):
    plt.subplot(2, 2, i)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.title(title)
    plt.axis("off")

plt.tight_layout()
plt.show()