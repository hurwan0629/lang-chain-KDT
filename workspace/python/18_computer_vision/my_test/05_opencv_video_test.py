import cv2
from pathlib import Path

VID_DIR = Path() / ".." / "movies"
IMG_DIR = Path() / ".." / "images"

vid_sea = cv2.VideoCapture(str(VID_DIR / "sea.mp4"))

cap = cv2.VideoCapture(0)

print("type(cap):", type(cap))
print("cap.isOpened()", cap.isOpened())
print("type(vid_sea):", type(vid_sea))
print("vid_sea.isOpened()", vid_sea.isOpened())


ret, frame = cap.read()
print(frame)
cv2.imshow("frame", frame)

cv2.imwrite(str(IMG_DIR / "hurwan01.png"), frame)

cv2.waitKey(0)
cv2.destroyAllWindows()

fps = vid_sea.get(cv2.CAP_PROP_FPS)
delay = max(1, round(1000 / fps))

cap.release()

while True:
    ret, frame = vid_sea.read()

    if not ret:
        print("vid_sea return is False")
        break

    frame = cv2.resize(frame, (240, 240))

    cv2.imshow("vid_sea", frame)

    if cv2.waitKey(delay) & 0xFF == 27:
        break
vid_sea.release()


