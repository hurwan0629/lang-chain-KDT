import cv2
import sys
from pathlib import Path

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("카메라를 잡지 못하였습니다.")
    sys.exit(0)

camera_fps = camera.get(cv2.CAP_PROP_FPS)
width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
delay = max(1, round(1000 / camera_fps))

# print(camera_fps)


print(" === camera info ===")
print("fps:", camera_fps)
print("frame delay:", delay)
print("width:", width)
print("height:", height)

VIDEO_DIR = Path() / ".." / "movies"

if not VIDEO_DIR.exists():
    print("video_dir path not exists")
    sys.exit(0)

record_save_path = str(VIDEO_DIR / "my_camera.avi")

fourcc = cv2.VideoWriter_fourcc(*"XVID")

print("save in:", record_save_path)
print("fourcc:", str(fourcc))
print("")

camera_record = cv2.VideoWriter(
    record_save_path,
    fourcc,
    camera_fps,
    (width, height)
)

while True:
    ret, frame = camera.read()

    if not ret:
        break

    # cv2.circle(
    #     frame,
    #     (round(width/2), round(height/2)),
    #     100,
    #     (0,0,0),
    #     3
    # )

    cv2.putText(
        frame,
        "esc를 눌러서 녹화를 종료하세요",
        (0, height),
        cv2.FONT_HERSHEY_COMPLEX,
        1.0,
        (0, 0, 0),
        3
    )

    cv2.imshow("camera", frame)

    camera_record.write(frame)

    if cv2.waitKey(delay) == 27:
        break

camera_record.release()
camera.release()
cv2.destroyAllWindows()

