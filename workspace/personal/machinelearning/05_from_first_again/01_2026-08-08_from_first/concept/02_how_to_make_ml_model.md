# 머신러닝의 전체 개요 [02] [검증 데이터 분할부터]

> 해당 글은 [머신러닝 전체 개요 1편](https://hurwan.tistory.com/78)에서 이어집니다.

## 5. 데이터 분할 전략 이어서
> 이전까지 `Hold-out`, `K-Fold`, `TimeSeriesSplit`, `Stratified split`, `Group Split`에 대해 다루었습니다.

### Repeated K-Fold
`RepeatedKFold`는 말 그대로 `K-Fold`를 여러번 다시 섞어서 반복하는 것을 말합니다. 파이썬 코드를 예로 들면 `random_state`를 여러종류로 돌려서 사용한다고 볼 수 있을거같습니다.

해당 방식은 `K-Fold`또한 결국 한번의 분할 이후 더이상 섞지 않기 때문에 이를 여러번 반복한다고 볼 수 있습니다.

해당 `RepeatedKFold` 클래스는 `sklearn.model_selection`모듈 에서 제공하고있으며 사용 방법은 다음과 같습니다.

```python
from sklearn.model_selection import RepeatedKFold

# 분할 전략
cv = RepeatedKFold(
  n_splits=5,
  n_repeats=3, # K-Fold를 반복하는 횟수
  random_state=42
)

scores = cross_val_score(
  model,
  X,
  y,
  cv=cv
)
```

해당 작업 시 `scores`는 총 길이 15짜리의 `int` 배열으로 나타납니다.

여러번 반복을 하기 때문에 모델 성능을 측정할 때 더 안정적이지만 연산 횟수가 늘어나 데이터가 과하게 크지 않은 경우에 사용하기 적합합니다.

> 여기에서 말하는 모델은 학습 전의 학습 알고리즘 및 모델 구조를 말합니다. (경우에 따라 Pipeline 전체를 모델로 취급하는 것도 가능합니다.)

### Leave-One-Out
`Leave One Out`  교차검증 방식은 줄여서 `LOOCV`라고 불리는 극단적인 `K-Fold` 방식이라고 이해할 수 있습니다.

예를 들어 데이터가 100개라면 99개의 데이터를 학습에 쓴 뒤 하나의 값을 예측하는데 사용하게 됩니다. 직관적으로 학습에 힘을 쏟은 뒤 한번의 예측을 통해 얼마나 잘 예측하는지에 대해서 다루게 되는데 이렇게 되면 학습에 쓰는 데이터 양을 단순하게 늘릴 수 있다는 점입니다. 

반대로 단점 또한 작지 않은데 데이터의 개수만큼 학습 및 검증 주기를 반복해야하기 때문에 계산양이 굉장히 크며 데이터 하나만을 검증을 하기 때문에 fold 점수도 굉장히 출렁일 수 있다는 문제가 존재합니다.

이에 따라 대체로 많이 사용하는 분할 기법은 아니며 `5-Fold`, `10-Fold`, `Repeated K-Fold`가 비교적 흔한 편입니다.

### Bootstrap
`Bootstrap`은 지금까지 비슷한 맥락을 가졌던 하나의 표본데이터를 잘라서 사용한다라는 개념과 다르게 원본 데이터에서 무작위의 데이터를 확인하고 다시 되돌려 놓는 것과 같은 분할 방식을 가집니다.

예를 들어 데이터가 `1, 2, 3, 4, 5`가 존재한다면 여기에서 `bootstrap sample`은 `1, 2, 2, 5, 5`와 같이 같은 데이터가 여러번 뽑힐 수 있으며 어떤 데이터는 아예 뽑히지 않을 수 있습니다.

여기에서 뽑히지 않은 값의 경우에는 `OOB`, `Out-of-Bag`라고 부르게 되며 위의 예시에서는 `3, 4`가 `OOB Sample`라고 할 수 있으며 이를 검증 데이터와 같이 사용할 수 있습니다.

> 부트스트랩 방식은 **복원추출**방식을 이용해서 여러개의 가짜 데이터셋을 뽑습니다. 이를 통해서 각 샘플이 달라짐에 따라 결과가 얼마나 변하는지를 관찰할 수 있게 됩니다. 이를 통해 확인이 가능한 것은 *모델이 얼마나 데이터 변화에 안정적으로 결과를 내나*를 볼 수 있습니다.

복원 추출방식은 `sklearn.utils`의 `resample`에서 사용할 수 있습니다.

```python
from sklearn.utils import resample

x_boot, y_boot = resample(
  X, y,
  replace=True, # 복원 추출을 의미
  n_samples=len(X), # 샘플에 들어가는 데이터의 개수
  random_state=42
)
```

> 위와 같이 코드를 짜게되면 하나의 샘플을 `n_samples`길이만큼 만들어준다고 볼 수 있습니다.

### ShuffleSplit
`Shuffle Split`은 `hold-out`를 여러번 랜덤하게 반복하는 방식입니다. 예를 들면 훈련 데이터셋과 검증 데이터셋을 `4:1`로 나눈다면 매번 다른 집합으로 나누는 것과 같다고 볼 수 있습니다.

`sklearn.model_selection`모듈의 `ShuffleSplit`을 통해 사용할 수 있습니다. 

```python
from sklearn.model_selection import ShuffleSplit, cross_val_score

cv = ShuffleSplit(
  n_splits=10,
  test_size=0.2,
  random_state=42
)

scores = cross_val_score(
  model,
  X,
  y,
  cv=cv,
)
```

## 6. 모델의 종류와 하이퍼 파라미터
앞에서 적절한 방식을 통해 데이터셋을 나누었으니 이제 적절한 학습 방식을 통해 데이터를 학습시키기 위해 모델과 그 모델이 학습하는 강도 또는 여러 요소들의 방식을 결정짓는 하이퍼파라미터에 대해 정리해보려 합니다.

