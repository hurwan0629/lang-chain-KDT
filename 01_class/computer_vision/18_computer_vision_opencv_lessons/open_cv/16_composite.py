from pathlib import Path
import matplotlib.pyplot as plt
import cv2
import sys
import numpy as np

print(Path().cwd())

VIDEO_DIR = Path() / ".." / "movies"

if not VIDEO_DIR.exists():
    print("비디오 디렉토리가 존재하지 않습니다.")
    sys.exit(0)

print("비디오 디렉토리:", VIDEO_DIR.cwd(), end="\n")

cap_background = cv2.VideoCapture(str(VIDEO_DIR / "sea.mp4"))
cap_woman = cv2.VideoCapture(str(VIDEO_DIR / "woman.mp4"))

if not cap_background.isOpened() or not cap_woman.isOpened():
    print("open failed")
    sys.exit(1)

cap_background_meta = {
    "width": cap_background.get(cv2.CAP_PROP_FRAME_WIDTH),
    "height": cap_background.get(cv2.CAP_PROP_FRAME_HEIGHT),
    "fps": cap_background.get(cv2.CAP_PROP_FPS),
    "frame_count": cap_background.get(cv2.CAP_PROP_FRAME_COUNT)
}

cap_woman_meta = {
    "width": cap_woman.get(cv2.CAP_PROP_FRAME_WIDTH),
    "height": cap_woman.get(cv2.CAP_PROP_FRAME_HEIGHT),
    "fps": cap_woman.get(cv2.CAP_PROP_FPS),
    "frame_count": cap_woman.get(cv2.CAP_PROP_FRAME_COUNT)
}

output_meta = {
    "width": 0,
    "height": 0,
    "fps": 0,
    "frame_count": 0,
}

for key in ["width", "height", "fps", "frame_count"]:
    output_meta[key] = min(cap_background_meta.get(key, 1), cap_woman_meta.get(key, 1))

delay = max(1, int(1000 / output_meta["fps"]))

print(output_meta)
print("delay:", delay)

# 마스크
lower_green = (35, 100, 100)
upper_green = (85, 255, 255)

while True:
    woman_ret, woman_frame = cap_woman.read()
    bg_ret, bg_frame = cap_background.read()

    if not woman_ret:
        break

    if not bg_ret:
        cap_background.set(cv2.CAP_PROP_POS_FRAMES, 0)
        bg_ret, bg_frame = cap_background.read()
        if not bg_ret:
            break

    # 두 영상 크기가 다르면 배경 영상을 전경 영상 크기에 맞춤
    bg_frame = cv2.resize(bg_frame, (woman_frame.shape[1], woman_frame.shape[0]))

    green_mask = cv2.inRange(cv2.cvtColor(woman_frame, cv2.COLOR_BGR2HSV), lower_green, upper_green)

    person_mask = cv2.bitwise_not(green_mask)

    # composite = cv2.copyTo(woman_frame, person_mask, bg_frame)
    composite = cv2.copyTo(bg_frame, green_mask, woman_frame)

    cv2.imshow("composite", composite)

    if cv2.waitKey(delay) & 0xFF == 27:
        break


# print(cap_background.get(cv2.CAP_PROP_FRAME_WIDTH))
# print(cap_background.get(cv2.CAP_PROP_FRAME_HEIGHT))
# print(cap_woman.get(cv2.CAP_PROP_FRAME_WIDTH))
# print(cap_woman.get(cv2.CAP_PROP_FRAME_HEIGHT))

cap_woman.release()
cap_background.release()
cv2.destroyAllWindows()
# fourcc = cv2.VideoWriter_fourcc(*"H256")
#
# while True:
#