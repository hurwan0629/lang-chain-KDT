import cv2
import sys
from pathlib import Path

VIDEO_DIR = Path() / ".." / "movies"

cap1 = cv2.VideoCapture(str(VIDEO_DIR / "232538_tiny.mp4"))
cap2 = cv2.VideoCapture(str(VIDEO_DIR / "276624_tiny.mp4"))

if not cap1.isOpened() or not cap2.isOpened():
    print("입력 동영상 중 하나 이상을 열 수 없습니다.")
    sys.exit()
else:
    print("모든 동영상이 정상적으로 열립니다.")

# 두 영상의 해상도 확인
for name, prop in [
    ("CAP_PROP_FRAME_WIDTH", cv2.CAP_PROP_FRAME_WIDTH),
    ("CAP_PROP_FRAME_HEIGHT", cv2.CAP_PROP_FRAME_HEIGHT),
    ("CAP_PROP_FPS", cv2.CAP_PROP_FPS),
    ("CAP_PROP_FRAME_COUNT", cv2.CAP_PROP_FRAME_COUNT)
]:
    print()
    if cap1.get(prop) == cap2.get(prop):
        print(name, "일치")
        print(cap1.get(prop))

    else:
        print(name, "불일치")
        print("cap1:", cap1.get(prop))
        print("cap2:", cap2.get(prop))

# fourcc(Four Character code)
# 4개의 문자로 동영상 코덱을 지정하는 코드
# JPEG와 같이 동영상을 압축하게됨
"""
1920x1080(x3) 해상도라고 할 때 =6,220,800byte = 6.2MB
1초에 30fps = 186MB
10초에 1860MB
1분 11.16GB

코덱 / 동영상 포멧

.mp4, avi, mov, mkv ... = 컨테이너 (동영상 파일 포멧)

코덱(압축하는 알고리즘):  영상을 압축하는 기술 (H264, H265, XVID, MJPEG, AVI

영상은 나오는데 소리가 안나오는 경우 또는 소리가 나오는데 영상이 안나오는 경우, 음성에 관련된 알고리즘과 이미지를 압축하는 알고리즘이 따로 있어서 그것을 묶어서 파일 포멧으로 관리함.

동영상 파일 포멧 = 동영상 압축 + 음성 압축 방식 + 자막 + 메타 정보

movie.mp4
MP4 컨테이너
Video: H.264
Audio: AAC
자막 / 시간정보 등 .. 

코덱의 종류
XVID, MJPG, 
H.264(H264), 
H.265/HEVC(H265), 
VP9, AV1
"""

width = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps1 = cap1.get(cv2.CAP_PROP_FPS)

print('너비: ', width)
print('높이: ', height)
print('FPS: ', fps1)

fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("mix.avi", fourcc, fps1, (width, height))

# print("fourcc exists:", hasattr(cv2, "VideoWriter_fourcc"))
# # 언패킹 문자열
# print(*"XVID")



if not out.isOpened():
    cap1.release()
    cap2.release()
    raise RuntimeError("출력 동영상 파일을 생성할 수 없습니다.")

delay = max(1, round(1000 / fps1))

for cap in (cap1, cap2):
    stop=False
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # width와 height를 2개 받게된다면 이 2개가 보여줄 화면과 동일한지 확인하기
        # 일치하지 않으면 강제 리사이징 해주기
        if frame.shape[1] != width or frame.shape[0] != height:
            frame = cv2.resize(frame, (width, height))

        out.write(frame)
        cv2.imshow("output", frame)
        if cv2.waitKey(delay) == 27:
            stop = True
            break
    if stop:
        break

cap1.release()
cap2.release()
out.release()
cv2.destroyAllWindows()