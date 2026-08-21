# [자유탐구] Pytorch의 구조와 여러 모델의 수학적 개념
> 이번에는 조금 Pytorch와 여러 모델들을 조금 더 깊이 자유롭게 알아보는 내용입니다.

# Pytorch
> Pytorch의 구조에 대해 알아봅니다.
1. Dataset/IterableDataset/DataLoader
2. Autograd 확장

## 1. Datatset
**Pytorch**의 **Dataset**는 단순한 인터페이스를 가지며 사용자가 자유롭게 해당 클래스를 상속한 커스텀 클래스를 생성할 수 있는 형태로 만들어져있으며, **DataLoader**의 경우에는 상대적으로 더 복잡한 형태를 가지고 있습니다.

`map-style Dataset`는 인덱스를 통한 접근을 하는 `iterable`한 속성보다 `mapping`의 특징을 더 가지고 있는 클래스입니다.

Dataset 클래스는 크게 `__len__`, `__getitem__` 매직메서드의 인터페이스를 제공하며 이는 Java의 `interface`와 다르게 `abc.ABC`, `@abstractmethod`를 통해 해당 메서드의 구현을 요청하는 형태가 됩니다.

반대로 **IterableDataset**은 `__iter__`을 중심으로 동작하게 됩니다.

이는 실제로 예제/실습에서는 많아봐야 n만 데이터셋인 경우 메모리에 적재가 수월하게 되는 경우가 많지만 `n`GB 이상의 데이터가 존재할 경우에는 `lazy loading`를 이용하여 특정 단위로 데이터를 필요할때마다 DB 등에서 데이터를 가져와야하기 때문에 보통 `__getitem__`과 `__iter__`, 그리고 **DataLoader**의 `__next__`를 이용하여 데이터를 필요할 때 로드하게 됩니다.

구분을 하면
- Dataset 구현체: `__len__`은 보통 한번에 로드하는 데이터 길이, `__getitem__`에서 저장되어있는 특정 인덱스 반환 또는 설계에 따라 인덱스와 매칭되는 DB 데이터 반환
- IterableDataset 구현체: `__iter__`을 이용하여 순차적으로 DB를 순회하며 데이터를 가져오게 됩니다. `__next__` 또는 `for` 등을 이용하여 꺼낼 수 있습니다.
- DataLoader: 생성자 인자중 dataset에 위의 구현체 2개 중 하나를 넣어주어 `tuple(Tensor[batch, n], tensor[batch_size, 1])`을 반환해주게 됩니다. 이때 두번째 텐서의 Size는 모델 출력에 따라 맞춰주게 됩니다.

> 결국에는 설계자의 역량에 따라 어느정도 자유롭게 변환이 가능합니다.

## 2. Autograd
**Autograd**는 `Tensor`에 수행된 연산을 실행하는 동시에 미분에 필요한 계산 그래프를 만들어주는 역방향 자동 미분 시스템입니다.

Forward를 실행할 때 토치의 Function 객체를 이용하여 DAG로 만들어주고 backward를 할 때 해당 그래프를 역으로 따라가면서 chain rule를 적용하게 됩니다.

이때 `leaf tensor` 이라는 그래프의 시작부분. 즉, 연산을 통해 만들어지지 않은 변수는 `grad_fn`을 가지지 않게됩니다.

예를 들면 $a=3x, b=a^2, L = b^2 + 1$ 에서 $x$에는 `grad_fn`가 존재하지 않습니다.

이는 여러 Function(Node) 구현체. 예를 들면 MulBackward0, ReluBackward0, MmBackward0 등이 존재하며 연산시에 자동으로 Node간에 각각의 이전 Node를 참조하며 그래프(DAG)를 그려주게 됩니다. 또한 backward메서드를 실행하는 시점에 Autograd Engine가 각 node의 backward를 재귀적으로 실행하는 형태가 됩니다.

> DAG는 Directed Acyclic Graph를 통해 무한루프가 존재하지 않는 그래프를 말합니다.

> backward는 재귀의 개념을 활용하여 그래프의 의존성을 관리하며 역방향으로 gradient를 전파하여 모든 gradient가 들어오면 다음 연산을 하는 방식을 사용합니다.

> 일반적으로 중간 텐서(non-leaf tensor)에 `.grad`가 영구히 저장되지 않고 쓰이고 버려지기 때문에 `Tensor.retain_grad()`을 통해 grad를 기록할 수 있습니다.

# 모델과 수학
> 모델에 들어가는 수학적인 시각을 확인합니다.

## 1. 활성화 함수의 필요
우선 간단하게 이야기 할것은 활성함수에 대해서입니다.

활성화 함수는 여러개의 선형변환만을 이용하면 결국 하나의 선형변환으로 만들 수 있기 때문에 중간에 비선형 함수를 섞어주는 방식을 말합니다.

간단한 2개의 선형변환을 섞어보면

$$f_1(x) = W_1x + b_1$$

$$f_2(x) = W_2x + b_2$$

$$f_2(f_1(x)) = W_2(W_1x + b_1) + b_2$$

$$ = W_1W_2x + W_2b_1 + b_2$$

형태가 되기때문에 $W'= (W_1W_2)$,  $b' = (W_2b_1 + b_2)$ 로 새로운 $f'(x) = W'x + b'$ 형태가 만들어지게 됩니다.

이를 해결하기 위해 특정 조건에 대한 비선형적인 조건을 다는 함수를 선형 변환 사이사이에 넣어주는 방식을 사용하게 됩니다.

## 2. 여러가지 활성화 함수
활성화 함수 또한 여러가지 종류가 존재합니다.

또한 활성화 함수도 미분의 대상이되는 수식을 만드는 주체가 됩니다.

### Sigmoid
시그모이드는 유명한 가로로 긴 S자 형태의 그래프로 다음과 같은 수식을 가집니다.

$$
\sigma(x) = \frac{1}{1 + e^-x}
$$

이를 통해 모든 실수 데이터를 정규화, $0 < z < 1$ 로 만들 수 있습니다.

시그모이드 함수의 경우에는 미분결과가 $\sigma(x)(1-\sigma(x))$ 이기 때문에 BCE의 손실함수와 궁합이 잘 맞습니다.

### ReLU
그냥 `max(0, x)` 으로 기억해도 될 정도의 단순하며 기본 `hidden layer`으로 선택하는 경우가 많습니다.

여기에서 기준점이 되는 `0`과 `y=x` 수식은 그냥 비선형 함수를 표현하기 쉬운 형태이기 때문이며 특별히 의미를 주지 않아도 모델이 어느정도 문제들은 학습을 통해 해결할 수 있습니다.

문제점 또한 존재하며 특정 뉴런의 가중치 결과가 모두 0 이하가 된다면 $ReLU(z) = 0, gradient = 0$이 되어 해당 뉴런에 대한 $weight$가 사실상 더 업데이트되지 않을 수 있습니다.

### Leaky ReLU
이는 음수를 아주 작은 음수값으로 설정하여 dead ReLU 문제를 해결하는 방식을 말합니다.

$$
f(z) =
\begin{cases}
z, & (z > 0) \\
\alpha z, & (z \le 0)
\end{cases}
$$

> 여기에서 $\alpha$는 음수의 크기를 줄이는 작은 숫지를 의미합니다.

### 깊은 신경망에서의 활성화 함수
활성화함수는 주로 미분값이 크게 나오지 않습니다. (보통 제곱, 1이상의 계수 등이 들어가지 않기 때문에)

이에 따라 미분 연산에 지속적으로 0.2, 0.01 등과 같은 작은 값들이 적용될 수 있으며 이에 따라 최종적인 학습이 가중치에 거의 적용되지 않을 수 있습니다.

### GELU
$GELU(x)$는 $xΦ(x)$을 의미합니다. 여기서 $Φ(x)$는 표준정규분포의 CDF임을 말합니다.

이는 음수는 부드럽게 억제하며 양수로 갈수록 점점 그대로 통과하게하여 미분 또한 매끄러운 형태로 구현할 수 있습니다.

![alt text](https://miro.medium.com/0*jetafLazYuwIXGuH.png)

### tanh
**tanh**은 **hyperbolic tangent**라고 불리는 `y=x` 대칭이동 한 탄젠트 함수와 유사하게 생겼습니다.

탄젠트의 수식은 다음과 같습니다.

$$
tanh(x) = \frac{e^x-e^{-x}}{e^x+e^{-x}}
$$

위 수식은 언제나 분모가 분자보다 큰 형태이며 원점 대칭 함수라는 것을 알 수 있습니다.

![tanh](https://img1.daumcdn.net/thumb/R800x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdna%2FdJc1QQ%2Fbtsq7cTVGzN%2FAAAAAAAAAAAAAAAAAAAAAJh5dsgFtqchWheTy0ZxSwYNohUp76cYPxm2TggidxTe%2Fimg.png%3Fcredential%3DyqXZFxpELC7KVnFOS48ylbz2pIh7yKj8%26expires%3D1788188399%26allow_ip%3D%26allow_referer%3D%26signature%3D1Uz%252Bh1pM52kXWKp9gq3m9O5K3GE%253D)

Tanh의 미분은 다음과 같습니다.

$$
\frac{d}{dx}\,tanh(x) = 1-\operatorname{tanh}^2(x)
$$

이는 $tanh(0)=0$ 일 경우의 $tanh'(0)=1$이 됨으로써 원점 근처에는 gradient가 잘 유지된다고 볼 수 있고, sigmoid의 미분 결과가 최대 0.25가 나와 gradient vanishing 되는것과 같이 $tanh$ 또한 gradient vanishing 문제를 가질 수 있습니다.

이는 $h_t = \operatorname{tanh}(W_2x_t + W_bh_{t-1} + b)$ 과 같이 내부 식이 과하게 커질 수 있는 경우, tanh을 이용하여 범위를 좁혀주는 기능을 넣어주게 되됩니다.
