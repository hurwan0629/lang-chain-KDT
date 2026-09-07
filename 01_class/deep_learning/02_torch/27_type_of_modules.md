# 여러 모듈의 종류

> 이번에는 신경망에서 쓰이는 여러 `nn.Module` 타입의 클래스들을 알아보겠습니다.

```python
import torch
from torch import nn
```

# 시작하기 앞서 알아둘 요소

## train/eval

`Module.train/eval`은 해당 모델과 그 하위의 모든 모델의 `training` 플래그를 바꾸며 그 값을 보고 동작을 달리하는 모듈들에 영향을 줍니다.

대표적으로

- `Dropout`모듈에서는 일부 값(노드/가중치 결과)을 확률적으로 0으로 만들어줍니다.
- `BatchNorm` 모듈에서는 train 시에는 현재 batch의 평균/분산을 사용하며 실시간으로 평균과 분산을 갱신하지만 eval 시에는 학습동안 저장된 값을 사용합니다.

## inference_mode

`torch.inference_mode()`를 동작시키면 해당 with 블럭 내에서 autograd 기능을 거의 완전히 종료시켜 메모리와 연산 오버헤드를 줄여줍니다.

이는 미분 그래프이자 비순환형 연산 그래프인 DAG를 만들지 않으며 일부 view 추적을 생략하며 version counter 관리를 생략하게 됩니다.

## no_grad/enable_grad/set_grad_enable

`inference_mode` 보다 좁은 범위의 기능으로 autograd DAG에 기록할지 말지를 설정합니다.

세개 모두 같은 설정으로 `set_grad_enable`가 두 메서드를 모두 포괄합니다.

- `with torch.no_grad():` - 연산을 DAG에 기록하지 않습니다.
- `with torch.enable_grad():` - 연산을 DAG에 기록합니다.
- `with torch.set_grad_enable(bool):` - 연산을 DAG에 선택적으로 기록합니다.

> 코드 블럭 안에서의 grad 상태 확인은 `torch.is_grad_enabled()` 로 확인이 가능합니다.

# nn.Linear

> 가장 대표적인 선형 변환 모듈입니다.

해당 모듈은 $W \cdot x + b$, 토치의 행벡터 형태로는 $xW^T + b$ 와 같은 형태의 모듈을 제공합니다.

기본적으로 W(weight)와 b(bias)는 파라미터 타입의 Matrix와 scaler 입니다.

`model`의 train/eval 상태에 따른 계산 차이는 존재하지 않으며 `inference_mode`에서는 다른 모듈과 동일하게 파라미터를 학습시키거나 DAG를 생성하지 않습니다.

```python
# 3차원을 2차원 데이터로 변환하여 반환
linear = nn.Linear(3, 2)

x = torch.randn(2, 3)


print("x.shape:", x.shape)
print("x:", x)

y = linear(x)

print()
print("y.shape:", y.shape)
print("y:",y)
print()
print("linear.weight.shape:", linear.weight.shape)
print("linear.bias.shape:", linear.bias.shape)
```

**출력**

```text
x.shape: torch.Size([2, 3])
x: tensor([[ 0.2480,  0.5469, -1.0453],
        [-0.6120,  0.2463,  0.3362]])

y.shape: torch.Size([2, 2])
y: tensor([[0.0053, 0.4547],
        [0.0441, 0.3433]], grad_fn=<AddmmBackward0>)

linear.weight.shape: torch.Size([2, 3])
linear.bias.shape: torch.Size([2])
```

# nn.Conv2d

> 대표적인 2차원 합성곱 모듈입니다. 4차원 (Batch, Channel, Weight, Height) 형태의 데이터를 받아 Channel의 개수와 Weight/Height를 padding/kernel의 값에 따라 다른 결과를 내보냅니다.

수식은 다음과 같습니다.

$$
y_{c_{out}} = \sum_{c_{in}} (W_{c_{out}, c_{in}} * X_{c_{in}}) + b_{c_{out}}
$$

> 위 수식을 설명하면 각 입력 채널들을 순회하며 각각의 채널들에 대해서 W(c_out, c_in, h, w)=kernel 을 선형곱 해주는 연산을 모두 진행 후 각각의 채널에 알맞는 가중치를 출력 채널만큼의 벡터를 합성곱 해주는 것을 말합니다.

선형결합과 비교하였을 떄 Weight의 차원이 1개 더 많다는 특징이 존재합니다.

batch_size=16의 batch, 8개의 channel, 256x128 이미지 데이터에서 weight(kernel 집합)의 형태는 (출력할 channel 개수, 8:입력 channel 개수, `len(kernel)`, `len(kernel)`) 의 형태를 가지게 됩니다.

여기에서 `len(kernel)`은 stride라고 불리는 커널의 행/열 개수를 뜻합니다.

또한 패팅은 가장자리 부분의 특징을 집중적으로 판단하기 위한 `0`으로 채워진 테두리를 뜻합니다. (개수를 선택할 수 있습니다.

train/eval 자체에는 영향을 받지 않습니다.

```python
conv = nn.Conv2d(
    in_channels=4,
    out_channels=16,
    kernel_size=4,
    padding=1
)

x = torch.randn(16, 4, 32, 32)

# 32 x 32 사이즈에서 (16=출력 채널)x(4=입력 채널)x(4x4 = 커널) 가중치를 가한 뒤 랜덤 bias를 더합니다.
# padding가 없다면 32 - 4 + 1 = 29로 29 x 29 사이즈가 되지만
# padding=1 을 통해 모든 방향으로 두께가 1 늘었기 때문에 +2 하여 31 x 31 사이즈가 됩니다.
y = conv(x)

print(y.shape)
print(y.grad_fn)
print(conv.weight.shape)
print(conv.bias.shape)
```

**출력**

```text
torch.Size([16, 16, 31, 31])
<ConvolutionBackward0 object at 0x0000019E1A384970>
torch.Size([16, 4, 4, 4])
torch.Size([16])
```

# nn.ReLU

> 대표적이고 많이 사용되는 기본적인 활성화 함수입니다.

개념적으로 `max(0, x)`와 동일하며 Tensor의 모든 원소에 대해서 독립적으로 적용되게 됩니다.

Autograd에서는 ReLU 연산이 기록되며 미분시에 ReLU 연산 시점에 0 이하인 값에 대하여 모든 미분 결과가 0이며 따라서

1. 선형변환
2. ReLU
3. 선형변환

과 같은 계산 과정에서 3번 미분 후 ReLU에서 미분시에 0이면 이후의 모든 미분 결과는 0이 되기 때문에 특정 파라미터의 해당 결과에 대한 가중치 누적은 0이 됩니다. (다른 여러 요소에 대한 미분 결과가 남기 때문에 가중치가 0이 된다는 의미와는 다릅니다.)

```python
relu = nn.ReLU()

# ReLU에는 파라미터가 없기 때문에 x에 requires_grad를 설정해주지 않으면
# y=relu(x) 를 했을 때 DAG 연산을 만들지 않음
x = torch.randn(2, 2, 2, 2, 2, requires_grad=True)

print((x < 0).sum())

y = relu(x)

print((y < 0).sum())
print(hasattr(relu, "weight"))
print(hasattr(relu, "bias"))
print(y.grad_fn)
```

**출력**

```text
tensor(15)
tensor(0)
False
False
<ReluBackward0 object at 0x0000019E570947F0>
```

# nn.BatchNorm2d

> 대표적인 2차우너 정규화(실제로는 표준화에 가까운) 모듈로 CNN에서 청규화 하는데 많이 사용됩니다.

n개의 입력 채널에서 각각의 채널에 대한 정규화(표준화에 가까운)를 합니다.

$$
\hat{x} = \frac{x-\mu}{\sqrt{\sigma^2+\epsilon}}
$$

$$
y = \gamma \hat{x} + \beta
$$

과 같은 수식이 만들어 질 때, $\gamma = weight$, $\beta = bias$ 와 같은 관계가 만들어집니다.

> $\mu$는 하나의 채널에 대응하는 하나의 batch의 모든 (H, W)의 평균을 의미하며, $\sigma^2$는 분산을 의미합니다.

이를 통해 BatchNorm은 단순히 스케일만 줄여주는거보다 조금 더 많은일 한다는 것을 알 수 있습니다.

- 중심 맞추기
- 분산 맞추기
- 크기와 위치를 조정해주기

> 또한 특별한점은 해당 모듈은 train/eval에 영향을 받는 요소인 Buffer타입의 running_mean, running_val을 가지며 학습시에 해당 두 값을 갱신해나가게 됩니다.

```python
bn = nn.BatchNorm2d(16)

# 8개 데이터, 16채널, 32x32 데이터
x = torch.randn(8, 16, 32, 32)

# (8, 1, 32, 32) 에 대한 정규화(표준화)를 진행합니다.
y = bn(x)

# 채널 개수만큼의 감마/베타, 평균/분산을 가져 채널별로 가중치를 다르게 설정합니다.
print(bn.weight.shape)
print(bn.bias.shape)

print(bn.running_mean.shape)
print(bn.running_var.shape)
```

**출력**

```text
torch.Size([16])
torch.Size([16])
torch.Size([16])
torch.Size([16])
```

# nn.Dropout

> Regularization 모듈로 한글로 규제 모듈입니다.

학습된 일부 값을 0으로 만들게 됩니다.

인자로 확률을 넣어주어 그 확률만큼 다른 규제되지 않은 값들을 $\frac{1}{1-p}$ 만큼 곱해주어 기댓값을 그대로 유지시켜줍니다.

train/eval 시에 비활성화 되는 모듈입니다.

```python
dropout = nn.Dropout(p=0.75)

x = torch.ones(10)

print(x)

print("\ndefault:", dropout(x))

dropout.eval()
print("\neval:",dropout(x))

dropout.train()
print("\ntrain:", dropout(x))
```

**출력**

```text
tensor([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])

default: tensor([0., 0., 0., 4., 0., 4., 4., 0., 4., 0.])

eval: tensor([1., 1., 1., 1., 1., 1., 1., 1., 1., 1.])

train: tensor([4., 0., 0., 0., 4., 0., 0., 0., 0., 0.])
```

# nn.MaxPool2d

> 영역에서 가장 큰 값만 가져옵니다.

보통 CNN에서 특징 추출을 할 때 피처맵의 크기를 줄여주기 위해 사용됩니다.

파라미터가 없으며 학습되는 모듈이 아닙니다.

주요 설정에는 다음과 같은 요소가 존재합니다.

- kernel_size: 한번에 볼 영역의 크기로 예를 들어 2로 설정하면 2x2 범위씩 탐방하여 그 중 하나의 값을 추출합니다.
- stride: 한번 계산 후 이동할 크기를 결정합니다. 기본값은 kernel_size와 같습니다.
- padding: 입력 가장자리에 `0`을 특정 두께만큼 추가합니다.
- ceil_mode: 정확히 나누어떨어지지 않아 남은 요소들을 확인할 것인지를 선택합니다.
- dilation : dilation이 `1`일 경우와 `2`일 경우에 각각 다음과 같이 탐색됩니다.

```text
dilation=1

X X X
X X X
X X X

dilation=2
X . X . X
. . . . .
X . X . X
. . . . .
X . X . X
```

```python
pool = nn.MaxPool2d(
    kernel_size=3,
    stride=3,
    ceil_mode=True
)

x = torch.randn(8, 16, 32, 32)

y = pool(x)

print(y.shape)
```

**출력**

```text
torch.Size([8, 16, 11, 11])
```
