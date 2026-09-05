import cv2
import numpy as np

img = np.full((500, 500, 3), 255, dtype=np.uint8)

oldx = 0
oldy = 0

def on_mouse(event, x, y, flag, param):
    """
    event: 발생한 마우스 이벤트 종류 객체
    x, y: 현재 마우스 좌표
    flag: 마우스 버튼이 눌렸는지 안눌렸는지 상태
    param: setMouseCallback()에서 전달한 추가 데이터
    """

    global oldx, oldy

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"왼쪽 버튼 DOWN: ({x}, {y})")
        oldx, oldy = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        print(f"왼쪽 버튼 UP: ({x}, {y})")
    elif event == cv2.EVENT_MOUSEMOVE:
        if flag & cv2.EVENT_FLAG_LBUTTON:
            print(f"드래그 중: ({x}, {y})")
            cv2.line(img, (oldx, oldy), (x, y), (255, 51, 255), 3)
            oldx, oldy = x, y
            cv2.imshow("canvas", img)


# print(img)
#            ndarray / 한쪽 꼭젓점(x, y), 한쪽 꼭짓점: (x, y) / (b, g, r), 두께
# 나중에 객체탐지에서 우리가 그리게 될 객체형태
cv2.rectangle(img, (50, 200), (200, 300), (255, 0, 0), 3)
cv2.rectangle(img, (300, 200), (400, 300), (255, 0, 0), -1)
cv2.circle(img, (150, 400), 50, (255, 0, 0), 3)

# 폰트 그리기       텍스트    위치                                       크기
cv2.putText(img, "Hello", (50, 100), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 5.0, (0, 0, 0), 1)

cv2.imshow("canvas", img)

# "canvas" 창에서 마우스 이벤트가 발생하면 onMouse 콜백을 호출한다.
cv2.setMouseCallback("canvas", on_mouse)

cv2.waitKey(0)
cv2.destroyAllWindows()

