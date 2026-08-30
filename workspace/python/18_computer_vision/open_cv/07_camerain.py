import cv2
import sys
import time

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("카메라를 열 수 없습니다.")
    sys.exit()

print("카메라 연결 성공")


width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
# 다른 속성으로는 CAP_PROP_FRAME_COUNT (전체 프레임수 - 카메라로는 안됨)
# CAP_PROP_POS_FRAMES (현재 프레임 위치)
# CAP_PROPS_POS_MSEC (현재 재생 위치)
fps = cap.get(cv2.CAP_PROP_FPS)

print("너비: ", width)
print("높이: ", height)
print("FPS:", fps)

# 카메라도 프레임을 가져와서 처리할 수 있음

while True:
    # ret, frame에 각각 bool, 프레임 화면이 나오며
    # 출력하는데는 가져오기 위한 시간을 가져오는 동기형 메서드
    ret, frame = cap.read()

    if not ret:
        print("카메라 프레임을 읽지 못했습니다.")
        break

    #
    cv2.imshow('camera', frame)
    # 키 입력을 기다리면서 OpenCV 창 이벤트도 처리하는 함수
    # 인자값을 핵심으로 가짐
    # 0이면 키가 눌릴 때까지 대기
    # 1000 이면 Nms만큼 대기
    # 1ms마다 키 입력을 남기고 돌아가기
    if cv2.waitKey(1) == 27:
        break

# 카메라/영상 장치에 대한 점유를 해제하는 메서드
cap.release()
cv2.destroyAllWindows()