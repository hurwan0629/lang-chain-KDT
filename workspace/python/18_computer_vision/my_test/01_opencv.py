import cv2
from pathlib import Path

# print(Path().cwd())

img_path = Path() / ".." / "images" / "dog.bmp"

print(img_path.cwd())

img = cv2.imread(img_path)

print(type(img))
print(img.shape)

cv2.imshow("show", img[::-1, :])

cv2.waitKey(0)
cv2.destroyAllWindows()

