# 전처리 할 때 카메라 위치에 의해 비스듬하게 읽어지거나 할 때
# 번호판을 잡아내어야 할 때, 한번 회전시키거나 이동시켜서 정상적으로 보이게 만들어주기
import cv2
import numpy as np
from pathlib import Path

IMG_DIR = Path() / ".." / "images"

img = cv2.imread(str(IMG_DIR / "dog.bmp"))

h, w = img.shape[:2]

"""
2 * 3 이동 변환 행렬

[ 1 0 tx ]
[ 0 1 ty ]
tx = x축 이동 거리
ty = y축 이동 거리

동차 좌표
"""

aff_translate = np.array([
    [ 1, 0, 150 ],
    [ 0, 1, 100 ]
], dtype=np.float32)

# 실제 이미지를 가져다가 특정 행렬 변환을 적용
dst_translate = cv2.warpAffine(img, aff_translate, (w, h))

print(dst_translate.shape)

# 크기 변경(Resize)
# 픽셀이 늘어나는 방식
# 보간(Interpolation): 이미 알고있는 주변 값들을 이용해서 중간에 필요한 값을 추정하는 것
# INTER_NEAREST: 최근접 이웃. 가장 가까운 픽셀 사용    (빠르지만 약간 손실이 존재함)
# INTER_LINEAR: 선형 보간. 주변 픽셀을 이용해서 계산   (빠르지만 약간 손실이 존재함) - 계단식 증가
# INTER_CUBIC: 3차 보간. 더 넓은 주변 픽셀을 이용해 부드럽게 계산
# INTER_AREA: 영역 보간. 축소할 때 주로 사용
dst_nearest = cv2.resize(img, (1280, 1024), interpolation=cv2.INTER_NEAREST)
dst_cubic = cv2.resize(img, (1280, 1024), interpolation=cv2.INTER_CUBIC)


# 회전 (Rotation)
center = (w / 2, h / 2)
# getRotationMatrix2D(회전 중심 좌표, 회전 각도, 확대/축소 비율)
# 회전 각도는 양수일 경우 반시계 방향으로 돌아감.
rot_matrix = cv2.getRotationMatrix2D(center, 30, 0.7)
dst_rotate = cv2.warpAffine(img, rot_matrix, (w, h))


cv2.imshow("dst_nearest", dst_nearest)
cv2.imshow("dst_cubic", dst_cubic)

cv2.imshow("original", img)
cv2.imshow("translate", dst_translate)
cv2.imshow("dst_rotate", dst_rotate)

cv2.waitKey(0)
cv2.destroyAllWindows()