import cv2
import sys

from pathlib import Path

print(Path().cwd())

video = Path() / ".." / "movies" / "232538_tiny.mp4"

print(video.exists())

# 인자에 0을 넣으면 카메라
# 경로를 넣으면 비디오
cap = cv2.VideoCapture(video)

if not cap.isOpened():
    print("동영상을 불러올 수 없습니다.")
    sys.exit()

print("동영상 로드 성공!")

width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps = cap.get(cv2.CAP_PROP_FPS)

print("너비: ", width)
print("높이: ", height)
print("프레임 수: ", frame_count)
print("FPS:", fps)

delay = max(1, round(1000/fps) if fps > 0 else 40)

while True:
    # ret: 프레임을 정상적으로 읽었는지 여부 (마지막에 읽게되면 False가 나옴)
    # frame: 읽어온 한 장의 영상 프레임(numpy 배열)
    ret, frame = cap.read()

    if not ret:
        break

    cv2.imshow("frame", frame)

    # delay 기다리고 넘어가기
    if cv2.waitKey(delay) == 27:
        pass

cap.release()
cv2.destroyAllWindows()