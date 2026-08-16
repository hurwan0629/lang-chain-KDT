# Pytorch 라이브러리 구조
> 파이토치의 내부 구조와 어떤 철학을 통해 만들어졌는지를 정리한 글입니다.

파이토치는 단순하게 연산을 빠르게 해주는 라이브러리보다 더 체계적인 모듈 구조를 가진 라이브러리입니다.

## 0. 빠르게 구조 확인하기

이 라이브러리의 주요 구성 요소를 빠르게 훑어보면 다음과 같습니다.
- `torch.Tensor`: `shape`, `dtype`, `device`, `autograd` 정보를 가진 `torch`의 주력 클래스
- `torch.autograd`: `Tensor`을 기반으로 `torch.autograd`를 통한 연산 그래프 사용 및 자동 미분 해주는 모듈
- `torch.nn`: 신경망 제작에 쓰이는 도구들을 모아둔 모듈
  - `.Module`: 모델/레이어의 기본 객체
  - `.Parameter`: 학습 대상이 되는 `Tensor`
  - `.Linear`: `Module`클래스를 상속한 선형 변환 클래스
  - `.ReLU`: `ReLU` 활성화 함수 클래스
- `torch.optim`: `Tensor.grad` 속성을 이용하여 `Parameter`을 수정해주는 도구를 모아둔 모듈
- `torch.utils.data`: `Dataset`, `DataLoader`과 같이 `batch` 또는 검증데이터 분할 등에 사용하는 모듈
> 추가로 **CUDA**등의 `backend`를 통한 **CPU**/**CUDA** 실제 연산이 이루어집니다. `Dispatcher`을 통해 올바른 연산 하드웨어를 사용하게 되며 내부의 **ATen**이라는 수학 연산 라이브러리를 통해 연산이 이루어집니다.

## 1. `torch.Tensor`
`pytorch` 라이브러리에서 쓰는 거의 모든 것에 사용되는 타입입니다.

보통 `torch.tensor([[1., 2.], [3., 4.]])` 과 같이 생성이 가능하며 차원, 모양, 내부 타입, 사용 하드웨어, 미분의 대상이 되는지, 어떤 연산을 통해 만들어지는지 (`grad_fn`) 등의 속성을 가지고 있습니다.

### 메서드 종류
기본적인 연산 단위 타입인 만큼 여러 메서드를 제공합니다.
- **형태확인**: 
  - `.shape`
  - `.size()`
  - `.dim()`
  - `.numel()`
- **형태변경**: 
  - `.reshape()`
  - `.view()`
  - `.flatten()`
  - `.unsqueeze()`
  - `.squeeze()`
  - `.t()`
  - `.T`
- **통계**: 
  - `sum()`
  - `mean()`
  - `max()`
  - `min()`
- **타입 또는 장치**: 
  - `.float()`
  - `.long()`
  - `.to()`
  - `.cpu()`
  - `.cuda()`
- **미분(`autograd`)**: 
  - `.backward()`
  - `detach()`
  - `.requires_grad`
  - `.grad`
  - `.grad_fn`
- **파이썬 기본타입**: 
  - `.item()`
  - `.tolist()` 

### 매직 메서드
파이썬 기능 덮어씌우기 정도로 생각할 수 있는 매직메서드 또한 텐서의 연산에서 구현되어있습니다.

예를 들어 텐서간의 `+`, `*`, `@` 등의 연산은 모두 메직메서드로 구현되어있습니다.

| 연산자 | 연산 대상 | 연산 방식 |
|---|---|---|
| `@` | 1차원 @ 1차원 | 내적 |
| `@` | 2차원 @ 1차원 | 행렬 벡터 곱 (연산을 위해 일시적으로 1차원에 빈 차원을 더하여 내적결과로 내보냄) |
| `@` | 1차원 @ 2차원 | 행렬의 벡터에 대한 선형 변환 |
| `@` | 2차원 @ 2차원 | 행렬곱 |
| `@` | n차원 @ n차원 | 각 텐서의 마지막 두 차원의 행렬곱 연산 |

`pytorch`의 `@`(`__matmul__`)연산은 내부적으로 여러 단계로 구성되어있어 `연산`, `dispatcher`(`cpu`, `cuda` 선택), 백그라운드 커널, 실제 물리 연산 등으로 진행되게 됩니다.

또한 `__getitem__`, `__eq__` 등의 경우에도 `numpy.ndarray`와 비슷하게 구현되어있습니다.

특별한 점으로는 `Tensor`의 인덱싱에서 `...`은 중간 차원을 모두 생략하는 `Ellipsis`라고 불리는 값으로 변환되어 지정하지 않은 나머지 차원을 전부 선택하라는 의미가 됩니다.

## 2. `torch.nn.Module`
`torch.nn.Module`는 모델 자체의 수식만 저장하는 것이 아닌 다음과 같은 작업을 총괄합니다.
- `submodules`관리 (내부에서 쓰는 모듈들)
- `Parameters`관리 (학습 대상이 되는 `Tensor`들)
- `train`/`eval` 상태 관리 (연산 시에 학습을 적용시킬지 확인)
- `buffer`, `hook`, `forward` 등 관리

이는 종적으로 여러 `Module`의 트리 구조로 구성될 수 있습니다.

해당 클래스에는 파라미터 텐서 배열을 꺼래는 `.parameters()`, `named_parameters()`(어떤 모델의 파라미터인지)가 존재하며, `.eval()`, `.train()`을 통해서 학습을 시킬지 또는 확인용 비학습 상태로 바꿀지를 선택할 수 있습니다. 또한 `.to(device)`를 통해 사용 장치를 선택이 가능합니다.

## 3. `torch.nn.Parameter`
해당 `Parameter` 클래스는 `Module`객체의 `weight`등의 타입으로 `Tensor`을 상속한 클래스라고 볼 수 있습니다.

이를 통해서 최상의 모델에서 `.parameters()`를 호출할 경우 호출 클래스에서 하위 모델로 재귀적으로 탐색을 해 지정된 파라미터를 제공하게 됩니다.

## 4. 연산 그래프
파이토치의 핵심적인 기능으로 예를 들어 

```python
logits = model(X_batch)
loss = torch.nn.BCEWithLogitLoss()(logits, y_batch)
```

와 같은 코드를 실행하면 `forward`를 계산하는 동시에 `autograd` 모듈을 통한 연산 기록을 저장하게 됩니다.

이는 `reverse-mode automatic differentiation` 시스템으로 실행된 연살들로 DAG(`Direct Acycle Graph`)를 동적으로 구성합니다. 

이를 통해 위 수식에서 `model` 객체에 등록되어있는 모든 수식에 `loss_fn` 수식까지 합하여 연산 순서 및 결과, 파라미터를 모두 `연산 node들의 그래프`로 저장하게 됩니다.

그래서 `list(model.parameters())[0][0][0]`과 같이 모델의 파라미터를 꺼내어 출력하게 되면 `tensor(0.1889, grad_fn=<SelectBackward0>)` 과 같은 형태로 출력이 되게 됩니다. 여기에서 `SelectBackward0` 가 바로 어떤 연산으로 해당 값이 나왔는지에 대한 값입니다.

파이토치는 내부적으로 이 연산과 연산결과를 통해 미분을 실행할 수 있게 됩니다.

## 5. TensorDataset과 DataLoader
검증데이터를 나누고 `batch`별 학습을 시키게되면 반드시 마주하게 되는 `torch.utils.data`의 `TensorDataset`과 `DataLoader` 클래스입니다.

`TensorDataset`의 경우에는 `TensorDataset(X, y)`와 같이 사용하여 이 둘을 튜플로 묶어주는 형태의 클래스이며 실제로는 원본 `Tensor`에 대한 인덱스를 지정해주는 객체정도의 역할을 합니다. (복사가 아닙니다.)

`DataLoader`의 경우에도 `batch`로 데이터를 나누기 위해서 아래와 같이 사용하게 됩니다.

```python
train_data_loader = DataLoader(
    train_dataset,
    batch_size=32,
    shuffle=True
)
```

이를 통해 `Iterable` 객체를 반환해주어 학습에 용이한 형태로 재구성해줍니다. (이 또한 복사가 아닙니다.)

