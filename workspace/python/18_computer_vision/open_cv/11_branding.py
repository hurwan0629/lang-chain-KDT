from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import sys

IMG_DIR = Path() / ".." / "images"

if not IMG_DIR.exists():
    print("이미지 디렉토리가 존재하지 않습니다.")
    sys.exit(0)
print("이미지 디렉토리:", IMG_DIR.cwd(), end="\n")

img1 = cv2.imread(str(IMG_DIR / "man.jpg"))
img2 = cv2.imread(str(IMG_DIR / "turkey.jpg"))

if img1.shape != img2.shape:
    raise ValueError(f"두 이미지의 shape가 다릅니다: {img1.shape}, {img2.shape}")

dst_numpy = img1 + img2
dst_opencv = cv2.add(img1, img2)

images = {
    "img1": img1,
    "img2": img2,
    "numpy": dst_numpy,
    "cv2.add": dst_opencv
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