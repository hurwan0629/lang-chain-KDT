import cv2
from pathlib import Path

print(cv2.__version__)

print("path:", Path())
print("path:", Path().cwd())
print("path:", Path().resolve())

profile = cv2.imread("../images/cchamppang.png", cv2.IMREAD_COLOR_BGR)

print("profile_size:", profile.shape)

cv2.imshow("my profile", profile)


cv2.waitKey(0)
cv2.destroyAllWindows()