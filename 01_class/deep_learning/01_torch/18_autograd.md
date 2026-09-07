# [PyTorch] PyTorch의 DAG와 chain rule
> PyTorch에서 미분 그래프가 어떻게 생기는지와 `chain rule`에 대해서 알아봅니다.

## Tensor
`torch.Tensor`에 존재하는 속성은 다음과 같습니다.
- 실제 데이터
- dtype
- device
- shape
- AutogradMeta
  - grad_
  - grad_fn_
  - grad_accumulator_
  - requires_grad
  - 기타 autograd 정보

여기에서 이는 PyTorch에서 사용하는 at::Tensor 내부 구현체를 말합니다. (나중에 C++ 레벨도 알아볼 예정입니다.)

## Module
`nn.Module`의 구현체는 자체 미분 그래프 Node를 말하지 않습니다.

Module 안에는
- 등록된 Parameter
  - weight
  - bias
- submodule
- buffer
- train/eval
- forward()

가 존재하게 됩니다.

이때 `forward()` 안에서 `x@W.T + bias` 등과 같은 연산이 실행되게 됩니다.

이때 Autograd에서는 forward 실행시에 필요한 연산 backward Node(미분용 연산 노드)를 만들게 됩니다.

이를 통해 `y = x@W.T + bias`가 실행되었을 때 `y.grad_fn`이 등록되게 됩니다.

이는 `=`, `@`, `+` 등과 같은 연산이 Tensor에서 오버라이딩되어 자동으로 `grad_fn` 생기게 됩니다.

`Loss = x**2` 라고 가정하겠습니다.

여기에서 $\operatorname{Loss}$를 미분하였을 때 $\frac{\partial L}{\partial L}$ 형태로 이루어지게 됩니다.

위의 값은 1이 되며, 이를 chaining rule에 의해 PowBackward0 을 역전파 하게 된다면

$\frac{\partial Loss}{\partial b} = 2b$ 가 되며 이때 b는 그대로 해당 역전파 시의 값을 넣어져 `2b` 가 자신의 grad에 누적되게 됩니다.

## forward부터 backward 전파까지
PyTorch에는 autograd라는 PyTorch의 자동 미분 시스템이 있습니다.

이는 단순히 클래스 또는 객체 등을 말하는 것이 아닌 Tensor연산이 일어날 때 그 연산에 대한 그래프를 만들고 Tensor.backward() 가 발생할 때 그 그래프를 역방향으로 실행하여 gradient를 계산해주는 기능 전체를 이야기합니다.

예를 들어서 다음과 같습니다.

```python
# 1. 모듈 사용
model = Linear(3, 1)

y = model(x)

# 2. 직접 연산
y = x@W.T + b
```

이 두 경우 모두 텐서의 연산으로 이루어지게 되며 이때 각 연산에 맞는 미분 그래프, DAG가 생성되게 됩니다.

이럴 경우 전체적인 미분 그래프는 다음과 같게 됩니다.

```
  y
  |
[add backward 연산 노드] ---- b
  |
[matmul backward 연산 노드]
 |      | 
 x    [Transpose backward 연산노드]   
          |
          W
```

또한 여기에서 `y.backward`를 수행하는 시점에 `add backward 연산 노드`에서 등록된 미분이 일어나게 되며 x 또는 b에 대해서 미분 값이 각각 전달되게 됩니다.

여기에서 파생되는 것이 `chain rule` 입니다.

`chain rule`는 여러 미분들이 `chain` 되어 실행되어 특정 변수에 대해서 $\operatorname{Loss}$의 값에 따른 기울기를 측정할 수 있는 미분식을 나타내는 방식을 말합니다.

예를 들어서 $L = l(f(W_2, g(W_1, x), b_2), target)$ 이라고 할 경우 각각의 변수 또는 가중치(파라미터)에 대해서 기울기를 구하기 위해선 앞에있는 모든 함수들에 대해서 미분을 할 필요가 있습니다.

따라서 다음과 같이 적용되게 됩니다

전재:

$$
g = g(W_1, x)
$$

$$
f = f(W_2, g, b_2)
$$

$$
L = l(f, target)
$$

미분: 

$$
\frac{\partial L}{\partial l} =1
$$

$$
\frac{\partial L}{\partial l} \frac{\partial l}{\partial f} \frac{\partial f}{\partial W_2} = W_{2.grad}
$$

$$
\frac{\partial L}{\partial l} \frac{\partial l}{\partial f} \frac{\partial f}{\partial b_2} = b_{2.grad}
$$

$$
\frac{\partial L}{\partial l} \frac{\partial l}{\partial f} \frac{\partial f}{\partial g} \frac{\partial g}{\partial W_1} = W_{1.grad}
$$

와 같은 형태로 체인이 되는 것을 말합니다.

이때 forward 할 때에는 Module 객체가 사용되지만 역전파시에는 Module가 관여되는 부분은 거의 없으며 내부에 사용되는 Parameter의 경우에는 따로 그래프(DAG)에 등록되어있어 자동으로 backward가 일어나게 됩니다.

> 저는 당연히 Module가 backward()를 시키는줄 알았는데 이 부분에서 생각과 오차가 있어서 이해하는데 시간을 사용하게 되었습니다.

# 마무리
이전동안 여러번 DAG, `chain rule`등을 언급하긴 하였지만 이번에 조금 더 확실하게 알아보는 시간을 가졌습니다.


개인적으로는 `C++` 구현을 더 파보고싶지만  

현재 논문을 읽을 기회가 생겨 그 글을 정리한 글을 작성해보려 하고있습니다.