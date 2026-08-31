# [머신러닝] OpenCV 시작
> 이번에는 OpenCV 진도를 시작함에 따라 복습할 겸 내용을 정리해보았습니다.

우선 OpenCV는 `Open Source Computer Vision Library`라는 컴퓨터가 사람의 눈처럼 이미지와 영상을 인식하고 처리할 수 있도록 돕는 오픈소스 컴퓨터 비전 라이브러리 입니다.

이는 이미지를 읽고 변환하는데 강점을 보이는 라이브러리입니다.

## 1. 이미지 읽기
기본적으로 `OpenCV`는 이미지를 읽는 기능을 제공합니다.

```python
import cv2

img = cv.imread("경로_문자열.png")

print(type(img))
# <class 'numpy.ndarray'>
```

또한 로딩 옵션으로 다음과 같이 설정 또한 가능합니다.

```python
# 컬러 이미지 로드
cv2.imread(path, cv2.IMREAD_COLOR)

# 흑백 이미지 로드 ([H, W)
cv2.imread(path, cv2.IMREAD_GRAYSCALE)
```

### 배열 순서

여기에서 반환값은 기본적으로 Numpy 배열로 컬러 이미지면 보통 `[H, W, C]` 형태로 반환되게 됩니다.

이러한 특징은 PyTorch의 `[C, H, W]` 형태와 대조되어 향후에는

```python
tensor = torch.from_numpy(img)
tensor = tensor.permute(2, 0, 1)
```

과 같은 코드가 나올 수 있습니다.

### BGR
OpenCV에서 채널의 기본 순서는 `{ 0: B, 1: G, 2: R }` 입니다. 

일반적으로 익숙한 순서는 `R G B` 순서이기 때문에 다음과 같은 방식으로 순서를 변환하여 시각화 할 때 사진이 이상하게 나오는 것을 막을 수 있습니다.

```python
rgb = cv2.cvtColor(
  img,
  cv2.COLOR_BGR2RGB
)
```

### dtype
또한 보통 이미지의 경우에는 `dtype=uint8`이며 픽셀 범위 `0~255`를 표현하게 됩니다.

PyTorch 모델에 넣을 때는 보통 `uint8`에서 `float32`타입으로 변환한 뒤 다시 `0~1`로 정규화 변환을 하게 됩니다.

```python
img = img.astype("float32") / 255.0
```

### `imread()` 실패
OpenCV는 `imread(path)`에 이미지가 없는 경우, 경우에 따라 예외 대신 `None` 값을 반환하게 됩니다.

따라서 다음과 같이 유효성 검사를 하는 것도 좋은 방법입니다.

```python
img = cv2.imread("???.jpg")

if img is None:
  print("image not exists")
```

## 2. 이미지 띄우기
OepnCV는 `imshow(panel_name, img_ndarray)`를 통해 화면을 그리는 기능을 제공해줍니다.

이때 띄워진 이미지 창은 프로세스의 종료와 함께 빠르게 종료될 수 있기 때문에 보통 키 입력을 기다리는 `waitKey()` 메서드와 함께 쓰이는 경우가 많습니다.

`waitKey()`의 인자로는 정수가 들어가며 `0`을 넣을 시에는 무한정으로 키 입력을 대기하며 `1` 이상을 넣을시에는 `N ms`동안 키 입력을 기다리고 다음 코드를 진행하게 됩니다.

`waitKey`의 반환값은 눌린 키 정보를 정수로 반환해줍니다. 이를 이용하여 `waitKey(0) == 27`과 같이 사용할 수 있으며 조금 더 보기 쉽게 하려면 `waitKey(0) & 0xFF == ord("q")` 패턴을 이용할 수 있습니다. (`0xFF`는 하위 8비트만 보기 위한 값입니다.)

`destroyAllWindows()`를 이용하여 OpenCV가 만든 GUI 창을 모두 닫을 수 있습니다. 특정 창만 제거하기 위해선 `cv2.destroyWindow("panel_name")`를 이용할 수 있습니다.

## 3. 영상 읽기
OpenCV에서는 영상 읽기 또한 제공하여 다음과 같은 코드를 이용하여 영상 매체 정보를 가져올 수 있습니다.

```python
# 파일 읽어오기
cap = cv2.VideoCapture("video.mp4")

# 웹 캠 읽어오기 (스트림 객체 번호)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
  print("video not detected")
```

또한 이후에는 `cap.read()`를 이용하여 `ret, frame` 값을 받을 수 있습니다.

`ret`는 `bool` 타입의 읽기 성공 여부 값이며 `frame`는 실제 한 프레임의 이미지 Numpy 배열입니다.

`ret`는 마지막 영상의 마지막 또는 카메라 프레임을 읽는 것에 실패하게 된다면 `False`를 반환합니다.

따라서 보통 `if not ret: brerak` `cap.read()` 아래에 넣습니다.

또한 마지막에 카메라를 잡은 경우에, 카메라를 계속 점유하지 않기 위해서 `cap.release()`를 작성할 필요가 있습니다.

또한 `cap.get(cv2.CAP_*)` 을 이용하여 `fps`, `width`, `height`, `frame_count` 등을 꺼낼 수 있습니다.

### fourcc
FourCC는 영상 코덱을 4글자 코드로 식별하는 값을 말합니다.

코덱이란 일반적으로 모든 프레임의 정보를 압축 알고리즘 없이 그대로 저장하면 용량이 너무 커지기 때문에 이를 codec를 이용하여 작언 영상으로 압축하여 보여주는 것을 말합니다.

영상에는 보통 영상 및 음성 데이터 모두 압축되어 저장되며 코덱의 종류로는
- `H.264`: 흔하며 호환성 좋음
- `H.265 / HEVC`: `H.264`보다 더 높은 압축률 + 높은 연산량
- `VP9`: 높은 압축 효율 및 최신
- `MJPEG`: 각 프레임을 JPEG처럼 압축. 단순하고 용량이 큼

이런 형태의 코덱들은 `fourcc = cv4.VideoWriter_fourcc(*"CODC")` 와 같이 사용할 수 있으며 `out = cv2.VideoWriter("mix.avi", fourcc, fps1, (width, height))` 와 같이 사용할 수 있습니다. 여기에서 확인할 것은 마지막의 인자 순서가 `(width, height)`라는 점입니다.

### cv2의 연산
`cv2`는 이미지에 대한 연산기능을 제공해줍니다.

- `cv2.resize(img, (w, h))`: 이미지를 리사이징 해줍니다.
- `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`: 2번째 속성을 이용하여 이미지의 색상 형식을 변경해줍니다.
  - `COLOR_RGB2GRAY`: RGB를 GRAY로 변경해줍니다.
  - `COLOR_BGR2RGB`: BGR을 RGB로 변경해줍니다.
- `cv2.flip(img, 1)`: 이미지를 뒤집어줍니다
  - `+1`: 좌우 반전
  - `0` : 상하 반전
  - `-1`: 상하 + 좌우
- `cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)`: 이미지를 회전시켜줍니다. `COUNTERCLOCKWISE`도 존재합니다.

아래와 같은 단순 연산 또한 존재합니다.
- `cv2.add(img_gray, 100)`
- `cv2.add(img_color, 100)`
- `cv2.subtract(img_gray, 100)`
- `cv2.multiply(img_gray, 2)`
- `cv2.divide(img_gray, 2)`