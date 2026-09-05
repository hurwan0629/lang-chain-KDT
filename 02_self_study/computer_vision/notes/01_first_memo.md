# [랭체인 수업] 컴퓨터 비전
> 이번에는 최근동안 수업의 전체적인 흐름을 다시 복기해보도록 하겠습니다.

## 1. OpenCV
OpenCV는 `.imread`, `VideoCapture` 등과 같은 메서드를 이용하여 외부 소스를 `numpy.ndarray`로 변환해줄 수 있는 기능을 제공해줍니다.

기본적으로 OpenCV에서의 이미지 데이터는 `(H, W)`가 채널의 앞부분에 존재하며 GrayScale의 경우에는 하나의 이미지의 `shape`가 (H, W)이며, BGR 이미지같은 경우에는 `(H, W, 3)`의 형태로 데이터가 저장되게 됩니다.

여기에서 `image` 3차원 배열에서 `axis=2`부분에는 순서대로 `[B, G, R]` 과 같은 데이터가 저장되게 됩니다.

*OpenCV는 기존에 존재하는 이미지를 영상을 처리하여 구조를 추출해 의미를 해석하기 쉽게 만드는 작업을 도와줍니다.*

OpenCV는 크게 4가지 역할을 해줍니다.
- 픽셀을 다루기 쉽게 만들어 이해하기 쉬운 구조로 만들게 됩니다. 이를 전처리라고 할 수 있습니다.
- 중요한 부분을 부각하여 경계선, 꼭짓점, 면적, 중심선 등과 같은 구조를 추출해낼 수 있습니다.
- 구조를 측정하여 해당 물체가 어디에 있는지, 기울어져있는지, 물체를 왜곡시키거나 이동시킬 수 있습니다.
- 이미지를 정형 정보를 변환하여 `json`, `xml`등과 같은 형태로 변환 시키는 것을 도와줍니다.

과거의 전통적인 Computer Vision은 사람이 특징(Kernel 도는 알고리즘)을 설계한 형태였습니다.

하지만 **역전파**와 함께 CNN의 kernel, FC layer의 가중치 및 여러 함수들에 대해서 컴퓨터가 이것을 직접 계산하는 형태가 되었습니다. 

이때 CNN에는 Conv 레이어라는 여러 특징 추출 계층이 존재하여 이미지를 굳이 전처리하지 않아도 알아서 분류해주지 않을까라는 생각이 들게됩니다.

물론 모델이 객체를 인식하는 것은 맞지만 그것을 계산하기 위한 구조로 만들어줄 필요가 있으며, 최종적으로 박스등을 그리고, 좌표를 계산하며 그것을 출력해주는 역할을 해주게 됩니다.

### `cvtColor` - 색상 공간
해당 메서드는 여러 색상 타입을 변환해주는 메서드입니다. 사용 방법은 `cv2.cvtColor(img, cv2.COLOR_기존형태2바꿀형태)` 의 방식으로 사용할 수 있습니다.

이 기능은 이미지를 출력하거나, `HSV`를 통한 이미지의 마스킹, `Gray`를 통한 이미지의 이진화 등을 위해서 사용되곤 합니다.

색상의 종류로는 크게 다음이 존재합니다.
- GrayScale: 밝기 정보만 존재하는 `(H, W)` 형태의 이미지 배열입니다. 한장당 2차원입니다.
- RGB/BGR: 빨강, 초록, 파랑 3채널에 대한 `numpy.ndarray` 를 하나의 요소로 가지는 이미지입니다. 3차원입니다.
- HSV: `Hue` 색상, `Saturation` 채도, `Value` 밝기로 나누어지며 색상 검출에 편한 형태입니다. 3차원입니다.
- HLS: `Hue`, `Lightness`, `Saturation`으로 나누어진 HSV와 비슷하지만 밝기 표현 방식이 다릅니다. 3차원입니다.
- YCrCb: `L` 발기, `Cb/Cr` 색차 정보를 이용하여 영상 압축, JPEC, 얼굴/피부색 처리 등에 많이 사용됩니다.
- Lab(CIELAB): `L`발기, `a` 초록과 파랑, `b` 파랑과 노랑을 이용하여 사람의 색인지 차이를 비교하기 좋은 형태입니다.
- XYZ: 여러 색 ㄱ공간의 기반이 되는 표준 색 공간입니다.

### `calcHist` - 픽셀 분포
하나의 이미지 데이터는 보통 `np.uint8`과 같은 형태로 저장되게 됩니다.

여기에서 `calcHist`를 이용하여 `np.uint8` 범위인 `0 ~ 256`부터 사용자가 선정한 이미지에 대해서 원하는 채널, 분포 범위, 나누는 구간의 개수 등을 선택할 수 있습니다.

> 픽셀의 분포를 확인하는 것은 대비가 낮은 이미지를 확인하기 위해서입니다. 

예를 들어 다음과 같이 사용 가능합니다.

```python
hist = cv2.calcHist(
  [img],     # 입력 이미지들
  [0],       # 사용할 채널
  None,      # 마스크 
  [256],     # 구간 개수
  [0, 256]   # 픽셀 값 범위
)

print(hist.shape) # (256, 1)
print(hist[122])  # 픽셀의 값이 122인 개수
```

여기에서 이미지를 시각화하기 위해 `matplotlib`를 사용하는 경우에, 다음과 같이 사용합니다.

```python
# 일반 BGR 이미지 출력 시
img = cv2.imread("img.jpg")

# matplotlib는 RGB 이미지를 기대하기 때문에 이미지 형식을 변환시켜줍니다.
img_rgb = cv2.cvtCoolor(img, cv2.COLOR_BGR2RGB)

# plt에는 상태기반 방식 (pyplot)와 객체 기반 방식 (fig, ax)가 존재하며 
# figure안에 존재하는 axes에 대해서 설정을 해주지만 plt.imshow()를 그대로 쓰면 자동으로 만들어서 동작하게 됩니다.
plt.imshow(img_rgb)
plt.axis("off")
plt.show()
```

GrayScale의 경우에는 따로 `cmap="gray"`로 지정해주게 되면 각 픽셀값에 대해서 회색으로 표현할 수 있게 됩니다.

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

plt.imshow(gray, cmap="gray")
plt.axis("off")
plt.show()
```

이때 채널간 픽셀 수 또는 GrayScale 한 채널에 대해서 픽셀 분포를 확인한 후 시각화를 하게 됩니다.

### 이진화
이진화는 데이터를 2가지 수준으로 나누는 것을 말합니다. 보통 `0`과 `255`로 나눠주게 됩니다.

`threshold` 라는 기준점이 되어주는 수치를 바탕으로 보통 검정색 또는 흰색으로 이미지를 분류하게 됩니다.

보통 이진화의 경우에는 회색조 이미지가 다양한 밝기를 내부적으로 가지고있을 대, 특정 픽셀이 찾는 대상에 대한 이미지인지, 배경에 속하는 이미지인지를 확인하기 위해서 이를 양 극단으로 나눠주게 됩니다.

여기에서 나오는 개념인 `threshold`(임계값)이 존재하며 해당 값을 기준으로 값을 `0` 또는 `255`로 나눠주게 됩니다.

사용하는 메서드는 다음과 같습니다.

```python
# 반환값 2가지
# 1. 실제로 사용한 threshold 값
# 2. 이진화된 이미지
threshold_value, img_bin = cv2.threshold(
  gray,   # GrayScale 이미지
  100,    # 기준 threshold
  255,    # 기준보다 클 때 넣을 값
  cv2.THRESH_BINARY   # 처리 방식
)

```

특히 마지막에 넣는 인자로는 몇가지 존재하며
- cv2.THRESH_BINARY: 지정한 threshold로 사용하는 값
- cv2.THRESH_BINARY_INV: threshold보다 높은 값을 `0`으로 만들고 작은 값을 `255`로 늘려주는 방식
- cv2.THRESH_OTSU: threshold를 사용자가 정하기 어렵기 때문에 히스토그램을 확인하고 적절한 경계값을 선택해주게 됩니다.

조명에 의해 위치에 따른 이미지의 지역에 따라 다른 분포를 가지게 된다면 `Adaptive Threshold`를 사용할 수 있습니다.

```python
img_bin = cv2.adaptiveThreshold(
  gray,   # GrayScale 이미지
  255,    # 조건 만족 시 넣을 값

  # adaptiveMethod
  cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # 가우시안 방식을 사용하여 픽셀마다 주변 영역을 보고 임계값을 계산하는 방식입니다. 이를 통해 가까운 픽셀의 영향을 더 많이 받습니다.
  # cv2.ADAPTIVE_THRESH_MEAN_C 또한 사용 가능합니다. 영역의 평균을 사용합니다.
  
  # thresholdType
  cv2.THRESH_BINARY,
  # cv2.THRESH_BINARY_INV 중에 선택이 가능합니다.

  11,   # blockSize: 확인할 주면 N*N 픽셀 값을 확인합니다.
  2     # C: 계산된 지역 threshold에서 빼줄 값을 구합니다. 
)
```
영역마다 `threshold`를 따로 계산하게 됩니다.

대표적인 알고리즘이 2가지가 존재하는데 `OTSU`는 threshold를 자동으로 찾는 알고리즘이며 `Adaptive Threshold`라는 영역별로 threshold를 다르게 잡는 것을 말합니다.

### 평활화 (Smoothing/Blur와 equalization)
평활화는 크게 2가지로 나누어 생각할 수 있습니다.
1. Smoothing/Blur: 커널을 이용하여 주변 픽셀에서의 급격한 변화를 줄이는 작업입니다.
2. Histogram Equalization: 히스토그램 분포를 넓혀서 색상 대비를 키우는 방식입니다.

대표적으로 평활화를 위한 Smoothing, Blurring은 다음과 같은 요소를 사용할 수 있습니다. 
- `cv2.blur()`, `cv2.boxFilter()`: 주변 픽셀 평균
- `cv2.GaussianBlur()`: 가까운 픽셀에 더 큰 가중치
- `cv2.medianBlur()`: 주변 픽셀의 중앙값

보통 이진화 전에 노이즈를 줄이기 위해 많이 사용합니다. 

히스토그램 평활화의 경우에는 픽셀 밝기의 분포를 높여 명암 대비를 높이며 다음과 같은 방식으로 사용이 가능합니다.

```python
eq_gray = cv2.equalizeHist(gray)
```

### Edge Detection - 이미지 경계선 추출
Edge Detection은 이미지에서 경계선을 찾는 작업을 말합니다.

보통 이미지의 픽셀이 급격하게 변하는 지점을 경계로 확인하게 됩니다.

사용하는 방식은
- Sobel: x, y축 방향의 밝기 변화량을 계산한 합니다.
- Laplacian: 2차 미분을 기반으로 변화가 큰 부분을 강조하게 됩니다.
- Canny: 실무/실습에서 매우 자주 사용하는 기법입니다.

다음과 같은 함수로 경계선을 추출할 수 있습니다.
```python
# threshold_1 이하로는 edge가 아니라 연결하며 threshold_2 사이의 범위에서 
# 강한 edge와 연결되어있으면 edge로 판단합니다.
edges = cv2.Canny(
  gray,   # GrayScale img
  100,    # threshold_1
  200     # threshold_2
)
```

자주 사용되는 흐름으로는 `Gaussian Blur`을 사용한 뒤, `Canny edge` 추출을 이용하여 안정적으로 경계선을 잡습니다.

이후 얻은 edge를 이용하여 `Contour 찾기`/`도형검출`/`객체 경계 분석` 등과 같은 작업을 이어갑니다.

### 윤곽선 추출
OpenCV에서는 객체의 윤관선 및 경계를 좌표들의 집합으로 추출하기 위하여 `cv.findContours` 메서드를 사용하게 되며 보통 인자에 들어가는 이미지로는 이진 이미지를 사용하게 됩니다.

```python
# 반환 값으로는
# contours: 윤곽선 (윤곽선 번호, 개수, 1, [x, y]) 형태가 들어있습니다.
# hierarchy: 각 윤곽선 정보에 대한 같은 레벨의 이전/다음 윤곽선 및 첫번째 자식, 부모 번호 또한 배열로 받을 수 있습니다.
contours, hierarchy = cv2.findContours(
  img_bin,
  cv2.RETR_EXTERNAL,  # 바깥쪽 경계를 반환합니다.
  cv2.CHAIN_APPROX_SIMPLE # 경계의 모든 점이 아닌 조금 더 단순화하여 반환시켜줍니다.
)
```

반환받은 `contour` 변수를 이용하여 다음과 같은 메서드에 사용이 가능합니다.
- cv2.contourArea(contour): 면적
- cv2.arcLength(contour, True): 둘레
- cv2.boundingRect(contour): 바운딩 박스
- cv2.approxPolyDP(): 꼭짓점 근사


### 마스크와 비트연산
`cv2.bitwise_*`과 같은 방식으로 연산을 할 수 있으며 

`cv2.copyTo(원본, 넣을_이미지_적용_마스크, 넣을_이미지)`와 같이 사용하여 이미지를 조작할 수 있습니다.

### 크기/좌표 변환
`resize`, `interpolation`, `warpAffine`, `warpPerspective` 등을 이용해서 기존 `x, y` 좌표를 이동시키는 방법에 대해서 나타냅니다.

각각 설정 알고리즘 또는 변환 방식을 설정할 수 있는 인자가 존재합니다.

### 필터링
`filter2D`, `blur`, `gaussianBlur`, `median` 블러 등을 이용하여 이미지를 조작할 수 있습니다.

### Morphology
`erode`, `dilate`, `open`, `close`를 이용하여 영역을 깎거나 키워서 사용할 수 있습니다.

### 객체 찾기
이미지를 이진화 시켜 안쪽에 존재하는 ConnectedComponents를 이용하여 윤곽을 나타내거나 크기를 구하거나 할 수 있습니다.

`findContours`는 객체의 경계를 찾아서 점들의 연속으로 만들어주게 됩니다.

