# How To Model AI machime
> 해당 글은 AI를 학습하는 과정과 그때 사용되는 `python` 라이브러리에 대해 다룹니다.

## 1. 머신러닝의 순서
머신러닝은 다음과 같은 순서를 통해 진행됩니다.
1. 데이터 준비
2. EDA
3. 데이터 전처리
4. 가설 설정
5. 모델 학습
6. 검증
7. 가설과 비교
8. 2번부터 다시 수정하며 모델 개선
9. 일정 수준의 모델이 생성되면 최종 테스트 진행

## 2. 문제 정의하기
AI는 실제 문제를 해결하기 위해 빠른 판단 기계를 만든다고 볼 수 있습니다.

해당 판단(추론)의 경우에는 크게 2가지 요소가 존재하며 이는 각각 `판단의 재료`(Feature)와 `예측하려는 결과`(target) 가 존재합니다.

여기에서 `feature`의 경우에는 보통 행렬의 형태로 이루어져 있으며 하나의 행은 데이터 하나를 의미하며 하나의 열(column)은 하나의 속성을 의미합니다. 

현재 작업중인 `House Price` 데이터의 경우에는 컬럼이 80개가 존재하며 층수, 얼마나 오래되었는지, 벽 마감재, 길거리 상태 등등이 존재하며 이를 기반으로 가격을 예측하는 데이터셋이 존재합니다.

## 3. EDA
EDA는 `Exploratory Data Analysis`라는 의미로 데이터가 어떤 형태로 존재하는지 확인하는 것을 말합니다. 예를 들어서 이번에는 (계속 `House Price`를 예시로 들겠습니다.) `MSSubClass`가 숫자 타입이였지만 범주형이거나 `NA` 수치가 구조적 결측인지 수치적 결측인지 확인을 하며 범주형 중에서도 카테고리별 비교가 가능한지, 주기형인지, 시간형인지 등등에 대해서 확인할 수 있었습니다.

## 4. 데이터 전처리
데이터를 나누는 경우에는 먼저 각 컬럼이 어떤 종류의 데이터인지 의미를 기준으로 분류하는 것입니다.

### 시멘틱 타이핑
첫번째로 `Semantic Typing`이라고 불리는 작업을 통해 해당 컬러럼이 어떤 데이터 유형인지 의미를 긱준으로 분류하는 것을 말합니다.

예시는 다음과 같습니다. `MSSubClass`의 경우에는 `int64` 타입이지만 실제로는 `Nominal Categorical`(명목 범주/비교 불가능 범주) 과 같으며 `GrLiveArea`또한 `int64` 타입이지만 실제로는 `Continuous Numerical`(연속적 숫자형)이 됩니다. 이 작업에 따라 `One-Hot Encoding`, `Ordinal Encoding`, `transforming` 등을 이용해서 데이터를 정리하고 결측치를 채울 것인지를 판단하게 됩니다.

#### 주요 시멘틱 타입
```
Numerical
├─ Continuous    연속형
└─ Discrete      이산형

Categorical
├─ Nominal       순서 없는 범주
└─ Ordinal       순서 있는 범주

Temporal         시간/날짜
└─ Cyclical      주기형

Identifier       식별자
```

### Missingness 의미 분류
위에서 언급하였듯 결측치의 경우에도 `없음`을 의미하기 위한 구조적 결측과 진짜로 값을 넣어놓지 못하여 발생하는 실실적 결측이 존재합니다.

예를 들면 `GarageType`가 결측치인 경우에는 `data_description.txt`에 없어서 결측치인 것이라 명시가 되어있지만 `LotFrontage` 같은 경우에는 도로 접면 길이라는 값이 존재하지만 찾아 넣지 못했음을 추측할 수 있습니다.

전자의 경우에는 그냥 결측치를 `"None"` 또는 `0` 등과 같이 한가지로 적절히 넣어주면 되고 후자의 경우에는 중앙값, `transformer` 등을 이용하여 적절한 값을 계산하여 넣는 것이 바람직 합니다.

### `scikit-learn`의 `SimpleImputer`
결측치를 채우는 것을 `Impute`라고 부릅니다. 또한 사이킷 런에서는 `sklearn.impute`라는 모듈을 제공합니다. 해당 모듈에는 `SimpleImputer`이 존재합니다. 해당 클래스는 `mean`, `median`, `most_frequent`, `constant` 같은 단순 전략을 인자로 줄 수 있습니다.

`SimpleImputer`의 경우에는 이름 그대로 인자로 준 `strategy`를 바탕으로 결측치를 채워주게 됩니다. 
1. `strategy="median"`을 넣어주면 중앙값을 기준으로 값을 채워주는 `SimpleImputer 객체`가 생성됩니다.
2. `imputer.fit(X)`를 통해 데이터를 확인하여 어떤 컬럼의 중앙값을 측정하게 됩니다. 여기에서 `SimpleImputer` 객체는 `X` 데이터를 학습했다고 표현합니다.
3. `imputer.transform(X)`를 이용하여 각가의 컬럼에 알맞는 결측치 대체값을 채운 `df` 객체를 반환해주게 됩니다. 
> 위의 과정은 `fit_transform(X)`을 통해 한번에 이루어질 수 있습니다.

> `Mode`는 최빈값을 의미하기도 합니다.

#### data leakage
여러 영상 또는 자료를 확인할 때 위와 같은 데이터를 다루는 클래스 및 객체를 사용하는 경우에는 테스트 데이터를 `fit()` 시키게 되면 해당 테스트 데이터를 내부적으로 전처리에 포함하게 되며 이를 *테스트 데이터를 학습했다* 라고 표현합니다. 또한 이것을 `data leakage`라고 부르게 됩니다. 따라서 **테스트 데이터셋은 학습 과정에서는 `transform()`에만 쓰는 것이 옳습니다.**

### `scikit-learn`의 `ColumnTransformer`
위에서 단순한 컬럼 결측치 처리 방식에 대해 다루었지만 컬럼별 데이터 분류 체계가 다른 경우에는 각각 다른 전략을 사용해야 할 수 있습니다. `numeric`의 경우에는 `median`을 사용할 수 있고, `nominal`의 경우에는 `most_frequent`, `ordinal`의 경우에에는 `OrdinalEncoder`을 사용해야 하기도 합니다.

이런 컬럼별 다양성을 받아내기 위해 `scikit-learn`은 `sklearn.compose` 모듈에서 `ColumnTransformer`을 제공해줍니다. 해당 컬럼은 `list[Tuple]` 타입을 인자로 받으며 리스트의 튜플에는 `("실행 이름", transformer객체, ["컬럼명", ...])` 과 같은 형태로 작성해야합니다.

`transformer 객체`는 `OneHotEncoder` 또는 `OrdinalEncoder`, `SimpleImputer` 등이 들어갈 수 있습니다.

### `scikit-learn`의 `StandardScaler`
일반적으로 머신러닝에서 숫자형 타입을 전처리할 때 정규화를 하게 됩니다. 특히 선형 회귀와 같이 거리나 계수의 크기, 최적화 과정을 사용하는 모델의 경우 전처리를 자주 사용하게 됩니다. 

`StandardScaler`은 `sklearn.preprocessing` 모듈에 존재하며 을 범주가 아닌 숫자형에 넣은건 그냥 학습할 때 ai가 단위나 절대적인 숫자의 크기 차이때문에 특정 컬럼들에만 비중 높게 모델이 나오는 것을 방지하기 위해 사용합니다.

### `scikit-learn`의 `Pipeline`
이제 자동화입니다. 데이터 전처리를 하는 경우에는 1가지보다 많은 과정을 실행할 수 있습니다.
1. 결측치 제거
2. 원핫 인코딩

이때 사용 가능한 도구가 `sklearn.pipeline`의 `Pipeline`입니다.

예를 들면 사용법은 다음과 같습니다.
```python
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer


# 범주형 컬럼 전처리 파이프라인
nominal_pipeline = Pipeline([
  ("imputer", SimpleImputer(strategy="most_frequent")), # 가장 많이 나온 값을 먼저 
  ("encoder", OneHotEncoder(handle_unknown="ignore")) # 원핫 인코딩 + ignore을 이용해서 모르는 타입은 무시하기 ([0, 0, 0] 과 같이 표현)
])

# 만든 파이프라인을 컬럼 변환기에 넣기
preprocessor = ColumnTransformer([
  ("nominal", nominal_pipeline, ["nominal_col_1", "nominal_col_2", "nominal_col_3"])
])
```

위에서 `ColumnTransformer` 하나를 실행하는 경우에 재귀적으로 내부에 들어있는 모든 코드가 실행되게 됩니다.

또한 위와 같이 만든 `ColumnTransformer`(`perprocessor`)은 그대로 `Pipeline` 객체 생성에 사용하여 다음과 같이 사용할 수 있습니다.

```python
from sklearn.linear_model import Ridge

model = Pipeline([
  ("preprocessor", preprocessor), # 앞에서 만든 컬럼 전처리 파이프라인(트랜스포ㅓ)
  ("regressor", Ridge())
])
```

## 5. 데이터 분할 전략 선택
사용할 모델을 선택하기 전, 데이터를 어떻게 분할할지에 대한 결정을 하게됩니다.

처음에 설명하였듯, AI 개발은 모델 생성 이후 검증 과정을 반복하게 됩니다. 이를 전문 용어로 **Model Develop Cycle** 또는 **Experimentation Loop**라고 부를 수 있습니다. 

#### 데이터의 큰 분류
데이터는 큰 분류로 `학습`, `검증`, `테스트` 데이터 셋으로 나뉘며 `테스트` 데이터셋은 마지막에 단 한번만 사용되며 한번 사용하는 순간 더이상 독립적인 최종 평가 데이터로 사용할 의미가 없어지게 됩니다. 테스트를 한 후 다시 모델을 만들게되면 그 다음으로 사용할 새로운 데이터를 찾을 필요가 있습니다.

### 데이터 분석이란
당연한 사실이지만 데이터로 존재하는 정보는 세상에 존재하는 정보의 일부일 뿐입니다. 그리고 캐글에서 가져오든 공공 데이터에서 가져오든 결국 그것은 세상에 있는 모든 데이터인 **모집단**의 일부일 분인 **표본**입니다.

> **AI 개발자들은 이러한 표본 데이터를 활용해 모집단을 추측해내는 것이라고 할 수 있습니다.**

그리고 이러한 표본들을 다시 세가지 분류의 데이터로 나누어 모델을 만들고, 추정을 하여 점수를 내게 됩니다. 이를 하나의 **추정량**이라고 표현합니다.

보통 통계학에서는 *표본을 통해 모평균 추정*을 하며 머신러닝에서는 *검증 데이터를 통해 일반화 성능을 추정*하게 됩니다.

### 검증 데이터 난이도에 따른 추정치 차이
일단 테스트 데이터는 미뤄두고 검증데이터를 먼저 살펴보겠습니다.

AI를 개발하는 경우에는 **검증데이터를 통해 모델이 얼마나 세상을 잘 표현하나**를 확인하게 됩니다. 이를 **일반화 성능**이라고 합니다. 

검증데이터는 모델 훈련 과정에서 모델이 얼마나 잘 만들어졌는지 개발자 또는 연구원이 확인할 수 있는 얼마 없는, 어떻게 보면 유일한 지표가 될 수 있습니다. 이때 검증 데이터가 컴퓨터에세 너무 상식적이며 예측하기 쉬운 데이터인 경우에는 성능이 좋게 추정되는 오류가 발생할 수 있고, 반대의 경우에는 실제 일반화 성능에 비해 낮은 결과를 표면에 나타낼 수 있습니다. 

이렇게 검증 데이터의 난이도에 따른 추정값 오류를 막기 위해 여러 **검증 데이터 분류 전략**이 나타나게 되었습니다.

검증 데이터 분류 전략에는 다음과 같은 종류가 존재합니다.
- `Hold-out`
- `K-Fold`
- `Group split`
- `Repeated K-Fold`
- `Bootstrap`
- `Stratified split`
- `Time-series split`

### Hold-out split
홀드 아웃 분할방법은 단순하게 검증 데이터를 떼어놓는 전략입니다. 

이는 `sklearn.model_selection`의 `train_test_split`을 통해 쉽게 구현할 수 있습니다.

> `model_selection`은 모델을 비교하고 선택하기 위한 평가 체계에 쓰이는 도구를 제공합니다.

이 방식은 단순하여 연산 비용이 굉장히 적고 (평가 한번) 빠르다는 것이지만 단순한 만큼 우연히 나오는 결과에 취약한 특징을 가지고 있습니다.

### K-Fold Cross Validation
위에서 `Hold-out split`의 약점을 보완하여 여러 조각으로 나누어 돌아가면서 평가하는 `K-Fold Cross Validation` 개념이 생겼으며, 이는 데이터가 100개가 있다면 몇조각으로 나눌 것인지 사용하여 돌아가며 검증을 하게 됩니다. 

예를 들어 데이터 100개, `n=5`로 설정하게 된다면 데이터들을 20개 단위로 나누어 5번에 걸쳐 학습과 검증을 진행하게 됩니다. `1 ~ 5` 번의 데이터 집합이 있으면 첫번째는 `1, 2, 3, 4`로 학습 후 `5`로 검증하며 두번째는 `1, 2, 3, 5`로 학습 수 `4`로 검증하는 절차를 가지게 됩니다.

이는 `sklearn.model_selection`의 `KFold`와 `cross_val_score`을 통해 구현이 가능하며 다음과 같이 작성하게 됩니다.

```python
from sklearn.model_selection import KFold, cross_val_score

cv = KFold(
  n_splits=5, # 5조각으로 나누기
  shuffle=True, # 나누기 전에 한번 섞을지
  random_state=42 # shuffle에 대한 시드 값
)

scores = cross_val_score(
  model, # 사용하는 모델 또는 파이프라인
  X,
  y,
  cv=cv
)
```

위 코드의 `scores`에는 각 `fold`의 점수 배열이 나오며 리스트 내부의 요소들에는 모델들의 `.score()`가 사용되게 됩ㄴ디ㅏ. 또한 `scoring="neg_root_mean_squared_error"` 등을 이용해서 직접 점수 방식을 선택할 수 있습니다.

### Stratified K-Fold
`Stratified K-Fold`는 `층화 K-Fold`라고 직역할 수며 각 `fold`에 `target`의 비율을 비슷하게 유지하는 것을 말합니다. 예를 들어 분류 문제에서 전체 데이터가 `정상 90%`, `이상 10%`로 나누어질 수 있는데 `K-Fold`는 경우에 따라 어떤 `fold`는 `정상 99%`, `이상 1%`가 나올 수 있으며 반대로 `정상 10%`, `이상 90%`와 같이 비대칭적으로 나올 수 있습니다.

이 작업은 `sklearn.model_selection`의 `StratifiedKFold`을 이용해 사용할 수 있으며 위에서 쓴 코드에 `KFold`를 `StratifiedKFold`로 바꾸기만 하면 사용할 수 있습니다.

하지만 이번에 사용한 `House Price` 데이터셋의 경우에는 회귀 문제이기 때문에 `KFold`를 사용하는 것이 자연스럽습니다.

> 물론 범위로 나누어 `Stratified K-Fold`를 사용할 수 있습니다.

### Group K-Fold
`Group K-Fold`는 같은 그룹에 속한 샘플이 `train`과 `validation`에 동시에 들어가면 안될 때 사용합니다. 

예를 들어 환자별 의료 데이터가 있는 경우에 `target`에 환자별 데이터가 각각 `10개`, `12개`, `20개`와 같이 들어있을 경우, 이런 것을 그룹별 (환자별로 나누어)로 나누는 것을 말합니다.

코드로 확인하면 다음과 같습니다.

```python
from sklearn.model_selection import GroupKFold, cross_val_score

cv = GroupKFold(n_splits=5)

patient_ids = [ # feature_df의 행 순서대로의 그룹 순서
    "A", "A", "A",
    "B", "B",
    "C", "C", "C",
]

scores = cross_val_score(
  model,
  X,
  y,
  cv=cv,
  groups=patient_ids
)
```

### Time Series Split
`Time Series Split`의 경우에는 시간 순서가 있는 데이터에 사용하는 데이터 분할 방식입니다.

일반적으로 주가, 날씨와 같은 과거를 보고 미래를 예측해야하는 경우에는 훈련용 데이터셋이 검증용 데이터셋보다 미래에 존재하면 해석에 오류가 있을 수 있기 때문에 항상 훈련용 데이터를 검증용의 과거시점으로 정렬하여 첫번째 테스트에는 `시점 [1] 훈련 후 시점 [2] 예측` 두번째에는 `시점 [1, 2] 훈련 후 시점 [3] 예측`, `...` 과 같은 누적 방식을 사용합니다.

`sklearn.model_selection`의 `TimerSeriesSplit` 에서 이전과 동일하게 `n_splits` 인자를 주어 교차검증이 가능합니다

# 다음에 계속
> 다음 포스팅에 이어서 작성하겠습니다.