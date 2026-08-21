# PyTorch Linear, ReLU, 역전파 및 Optimizer 내부 구조 확인
> 이번 포스팅에서는 직접 객체들의 타입, 속성, 메서드등을 통해 상태를 확인하며 한번의 학습 과정을 돌려보겠습니다. 이번 공부의 목표는 `Pytorch` 내부 타입 구조를 눈으로 익히며 메서드들의 동작을 더 명확히 아는 것입니다.


torch의 tensor 메서드를 이용하여 배열을 Tensor 객체로 생성해줍니다.
해당 크기는 `torch.Size([2, 2])` 형태로 출력됩니다.

### input

```python
import torch
from torch.nn import Linear, ReLU
from torch import nn, Tensor

x = torch.tensor([
    [2.0, 3.0],
    [1.0, -2.0]
])
```

linear 모델에는 2가지 기본 인자가 존재합니다.

* `in_features`: 입력 벡터의 특성 개수
* `out_features`: 출력 벡터의 특성 개수

### input

```python
linear = nn.Linear(
    in_features=2,
    out_features=3
)

print(x)
# Linear을 출력시에는  입력/출력 벡터 크기와 함께 가중치 여부가 기록됩니다.
print(linear)
```

### output

```text
tensor([[ 2.,  3.],
        [ 1., -2.]])
Linear(in_features=2, out_features=3, bias=True)
```

## Linear 내부의 weight와 bias

내부적으로 존재하는 모든 가중치를 행렬 형태로 출력합니다.

결과는 `[out_features, in_features]` shape의 배열입니다.

기본 행렬곱인 `[in_features, out_features]` 형태가 아닌 이유는 `PyTorch`에서의 열벡터를 한 행으로 나타나기 때문입니다.

곱하면 모든 `[in_features]` 크기의 벡터와 입력 벡터의 내적을 `[out_features]`번 하게 됩니다.

실제 계산에서는 `x @ W.T + b` 형태로 전치하여 사용합니다.

```python
print("weight:")
print(linear.weight)

# 결과는 `[out_features]` shape의 배열입니다.
print("\nbias:")
print(linear.bias)

# 크기를 반환합니다.
print("\nweight shape:")
print(linear.weight.shape)

print("\nbias shape:")
print(linear.bias.shape)
```

### output
```text
weight:
Parameter containing:
tensor([[ 0.0706, -0.5220],
        [-0.2757,  0.2802],
        [-0.4189, -0.5543]], requires_grad=True)

bias:
Parameter containing:
tensor([-0.5124, -0.2307, -0.1315], requires_grad=True)

weight shape:
torch.Size([3, 2])

bias shape:
torch.Size([3])
```

## weight와 bias 직접 변경

`requires_grad=True` 인 파라미터 weight, bias 를 바꿉니다.

이때 `=` 또한 텐서에 대한 연산이기 때문에 **Autograd**가 추적하려합니다.

이를 막기 위해 `torch.no_grad()`를 한 뒤 작업 완료 후 자동으로 닫아주게 합니다.

```python
with torch.no_grad():
    # 첫번째 차원만 모두 선택하면 나머지 차원이 모두 선택되게 됩니다..
    # 여기에서 weight객체 자체는 바꾸지 않을 것이기 때문에 내부의 요소를 바꾸게 합니다.
    linear.weight[:] = torch.tensor([
        [1.0, 0.0],
        [0.0, 1.0],
        [1.0, -1.0],
    ])

    linear.bias[:] = torch.tensor([
        0.0,
        1.0,
        0.0
    ])
```

이렇게 되면 현재는 계산 시에

```text
입력: x =
      [2, 3]
      [1, -2]

출력: y =
      [2, 4, -1]
      [1, -1, 3]
```

이 나오게 됩니다.

`weight`는 이전 블로그에 올렸듯이 `parameter` 모듈의 `Parameter` 타입입니다.

```python
type(linear.weight)
```

## Linear Module model 돌려보기

```python
z = linear(x)
```

결과에서는 tensor과 함게 어떤 연산을 통해 해당 값이 만들어졌는지 나오게 됩니다.

`AddmmBackward0` 의 경우에는 **행렬곱 + 덧셈 연산의 역전파 노드**를 뜻합니다.

### input

```python
print(z)
print(z.shape)
```

### output

```text
tensor([[ 2.,  4., -1.],
        [ 1., -1.,  3.]], grad_fn=<AddmmBackward0>)
torch.Size([2, 3])
```

### input

```python
print(type(z))
print(z.grad_fn)
```

### output

```text
<class 'torch.Tensor'>
<AddmmBackward0 object at 0x0000026F5CE82020>
```

## 직접 행렬곱 계산하기

pytorch에서 batch 데이터의 `x`의 shape는 보통 `[batch, features]` 형태를 가지게 됩니다.

수동으로 작업을 하기 위해선 행렬곱 이전에 weight를 올바른 선형 변환 행렬로 바꾸어주어야합니다.

이를 위해서 전치(transpose)를 걸어주며, `x @ W.T` 의 결과는 `tensor.Size([2, 3])` 이 되며 `linear.bias` 의 크기는 `tensor.Size([3])` 이기 때문에 자동으로 브로드캐스팅 되어 `[2, 3]` 으로 늘어나게 됩니다.

```python
manual_z = x @ linear.weight.T + linear.bias
```

동일하게 직접 계산하여도 AddBackward0 결과가 나오게 됩니다.

### input

```python
print(manual_z)

# 두 값이 유효범위 내에서 같은지 비교합니다.
print(torch.allclose(z, manual_z))
```

### output

```text
tensor([[ 2.,  4., -1.],
        [ 1., -1.,  3.]], grad_fn=<AddBackward0>)
True
```

## ReLU

ReLU는 Activation Function(활성화 함수)입니다.

`max(0, x)` 정도로 해석이 가능하며 여러 선형결합이 하나의 단순한 선형변환으로 나타내는 것을 막기 위해 사용됩니다.

### input

```python
relu = nn.ReLU()

h = relu(z)

print("before ReLU")
print(z)

print("\nafter ReLU")
print(relu(z))
```

### output

```text
before ReLU
tensor([[ 2.,  4., -1.],
        [ 1., -1.,  3.]], grad_fn=<AddmmBackward0>)

after ReLU
tensor([[2., 4., 0.],
        [1., 0., 3.]], grad_fn=<ReluBackward0>)
```

`torch.nn.ReLU`에는 `torch.nn.Linear` 에 존재하는 parameter 값이 존재하지 않습니다.

### input

```python
print("linear.parameters():\n", list(linear.parameters()))
print("\n\nrelu.parameters():\n", list(relu.parameters()))
```

### output

```text
linear.parameters():
 [Parameter containing:
tensor([[ 1.,  0.],
        [ 0.,  1.],
        [ 1., -1.]], requires_grad=True), Parameter containing:
tensor([0., 1., 0.], requires_grad=True)]


relu.parameters():
 []
```

## 라이브러리 구조

`torch.nn.modules` 내부의 `.linear.Linear` 타입임을 알 수 있습니다.

주요 속성으로는 파라미터, 버퍼, 입출력 크기, `_backward_pre_hooks`, 등이 존재합니다.

### input

```python
print(type(linear))
print(linear.__dict__.keys())
```

### output

```text
<class 'torch.nn.modules.linear.Linear'>
dict_keys(['training', '_parameters', '_buffers', '_non_persistent_buffers_set', '_backward_pre_hooks', '_backward_hooks', '_is_full_backward_hook', '_forward_hooks', '_forward_hooks_with_kwargs', '_forward_hooks_always_called', '_forward_pre_hooks', '_forward_pre_hooks_with_kwargs', '_state_dict_hooks', '_state_dict_pre_hooks', '_load_state_dict_pre_hooks', '_load_state_dict_post_hooks', '_modules', 'in_features', 'out_features'])
```

## named_parameters()

`linear.named_parameters()` 는 제너레이터 객체입니다.

선형 모델에는 2개의 파라미터가 존재하며 각각 weight와 bias 입니다.

제너레이터는 크게 파라미터 이름과 파라미터 객체를 줍니다.

`torch.nn.parameter.Parameter`은 기본적으로 `requires_grad=True`인 Tensor의 특수 형태라고 볼 수 있습니다.

또한 optimizer가 학습의 대상으로 받아갈 대상이 됩니다. `(param)`

### input

```python
print("linear.named_parameters():", linear.named_parameters())

for name, param in linear.named_parameters():
    print(name)

    # torch.nn.parameter.Parameter
    print(type(param))

    # 실제 weight 또는 bias의 Size
    print(param.shape)

    # Autograd의 추적 여부
    # Autograd는 미분 시스템/엔진으로 Tensor들과 연산 노드들이 연결된 동적 그래프를 만듭니다.
    print(param.requires_grad)

    print()
```

### output

```text
linear.named_parameters(): <generator object Module.named_parameters at 0x0000026F5CE4E940>
weight
<class 'torch.nn.parameter.Parameter'>
torch.Size([3, 2])
True

bias
<class 'torch.nn.parameter.Parameter'>
torch.Size([3])
True
```

## state_dict()

Linear Module 타입의 기억하고있는 학습 상태를 딕셔너리 형태로 꺼내는 메서드입니다.

### input

```python
print(linear.state_dict())
print(linear.state_dict().keys())
```

### output

```text
OrderedDict({'weight': tensor([[ 1.,  0.],
        [ 0.,  1.],
        [ 1., -1.]]), 'bias': tensor([0., 1., 0.])})
odict_keys(['weight', 'bias'])
```

## 직접 커스텀 Module 만들기

pytorch에서 제공하는 `torch.nn.Module`를 이용하여 직접 커스텀 Module을 만들 수 있습니다.

```python
# 이번 코드에서 실제로 사용되지 않습니다. 
class MyModel(torch.nn.Module):

    def __init__(self):
        super().__init__()

        self.ln1 = nn.Linear(2, 3)
        self.ru1 = nn.ReLU()
        self.ln2 = nn.Linear(3, 1)

    def forward(self, X):
        return self.ln2(
            self.ru1(
            self.ln1(
                X
            )))
```

## Sequential

```python
model = nn.Sequential(
    nn.Linear(2, 3),
    nn.ReLU(),
    nn.Linear(3, 1)
)
```

`torch.nn.container.Sequential` 타입입니다.

`Sequential.named_modules()`을 출력하면 최상위 모델부터 아래로 리스트로 반환하는 제너레이터를 반환하게 됩니다.

여기에서 가장 먼저 이름 없는 `''` Sequential 객체가 나오고ㅓ 두번째로 그 하위의 모델들이 순서대로 출력되어 `[0. Sequential 1. Linear1 2. ReLU2 3. Linear2]` 가 반환되게 됩니다.

### input

```python

print(type(model))

print("\nmodel names")

print(list(model.named_modules()))
```

### output

```text
<class 'torch.nn.modules.container.Sequential'>

model names
[('', Sequential(
  (0): Linear(in_features=2, out_features=3, bias=True)
  (1): ReLU()
  (2): Linear(in_features=3, out_features=1, bias=True)
)), ('0', Linear(in_features=2, out_features=3, bias=True)), ('1', ReLU()), ('2', Linear(in_features=3, out_features=1, bias=True))]
```

내부에 등록되어있는 Parameter을 순서대로 반환해주는 제너레이터를 왁인하겠습니다.

Linear모델이 2개 등록되어있어 `0.weight`, `0.bias`, `2.weight`, `2.bias` 순서로 출력되게 됩니다.

### input

```python
print(model.named_parameters())

print("\nmodel params")

print(list(model.named_parameters()))
```

### output

```text
<generator object Module.named_parameters at 0x0000026F5CE4E640>

model params
[('0.weight', Parameter containing:
tensor([[-0.4693, -0.6303],
        [ 0.2238,  0.1087],
        [-0.4982,  0.5043]], requires_grad=True)), ('0.bias', Parameter containing:
tensor([ 0.4101, -0.4195,  0.2183], requires_grad=True)), ('2.weight', Parameter containing:
tensor([[ 0.2860,  0.3570, -0.5004]], requires_grad=True)), ('2.bias', Parameter containing:
tensor([-0.5282], requires_grad=True))]
```

`Sequential.state_dict()`는 학습된 상태를 딕셔너리로 내보냅니다.

```python
print(type(model.state_dict()))
print(model.state_dict())
```

```text
<class 'collections.OrderedDict'>
OrderedDict({'0.weight': tensor([[-0.4693, -0.6303],
        [ 0.2238,  0.1087],
        [-0.4982,  0.5043]]), '0.bias': tensor([ 0.4101, -0.4195,  0.2183]), '2.weight': tensor([[ 0.2860,  0.3570, -0.5004]]), '2.bias': tensor([-0.5282])})
```

## 학습 데이터

```python
X = torch.tensor([
    [1.0, 2.0],
    [2.0, 1.0],
    [3.0, 4.0],
    [4.0, 3.0],
])

y = torch.tensor([
    [3.0],
    [3.0],
    [7.0],
    [7.0],
])
```

## 예측과 Loss

### input

```python
y_pred = model(X)

print(y_pred)

loss_fn = torch.nn.MSELoss()

loss = loss_fn(y_pred, y)

print(loss_fn)
```

### output

```text
tensor([[-0.8851],
        [-0.4794],
        [-0.6537],
        [-0.2419]], grad_fn=<AddmmBackward0>)
MSELoss()
```

## Sequential 객체에서 모델 하나씩 꺼내기

Sequential 객체에서 모델을 하나씩 꺼내서 사용해줍니다.

위와 동일한 결과가 나오는 것을 확인할 수 있습니다.

### output

```python
y_1 = model[0](X)
y_2 = model[1](y_1)
y_3 = model[2](y_2)

print(y_3)
print(loss(y_3, y))
```

### input

```text
tensor([[-0.8851],
        [-0.4794],
        [-0.6537],
        [-0.2419]], grad_fn=<AddmmBackward0>)
tensor(34.5561, grad_fn=<MseLossBackward0>)
```

## backward()

loss 을 이용해서 수식에 들어간 모든 requires_grad 객체 (Parameters) 편미분 후 각각의 grad 에 넣어줍니다.

각각 Parameter의 grad 속성을 확인하여 편미분 결과 상태를 확인합니다. (기울기)

이때 역전파 과정은 `Loss -> Ln2 -> ReLU -> Ln1` 으로 가기 때문에 bias에도 적절한 미분값이 생기게 됩니다.

### input

```python
loss.backward()

for n, p in model.named_parameters():
    print(n, "- grad")
    print(p.grad)
```

### output

```text
0.weight - grad
tensor([[  0.0000,   0.0000],
        [-11.2061, -11.3520],
        [  6.7165,   9.6033]])
0.bias - grad
tensor([ 0.0000, -3.9738,  2.8868])
2.weight - grad
tensor([[ 0.0000, -5.8122, -4.2510]])
2.bias - grad
tensor([-11.1300])
```

### input

```python
print(model.state_dict())
print(X)
```

### output

```text
OrderedDict({'0.weight': tensor([[-0.4693, -0.6303],
        [ 0.2238,  0.1087],
        [-0.4982,  0.5043]]), '0.bias': tensor([ 0.4101, -0.4195,  0.2183]), '2.weight': tensor([[ 0.2860,  0.3570, -0.5004]]), '2.bias': tensor([-0.5282])})
tensor([[1., 2.],
        [2., 1.],
        [3., 4.],
        [4., 3.]])
```

## dead ReLU

해당 결과에서 1번 Linear 함수에서 첫번재 뉴런의 결과는 X의 모든 데이터에 대해서 음수입니다.

이는 곧 ReLU 활성화 함수가 결과들을 모두 0으로 변환하는 것을 의미하며 해당 뉴런은 더이상 일반적인 목적함수를 이용하여 업데이트되지 못하는상태가 됩니다.

이를 뉴런이 **dead ReLU**가 되었다고 표현합니다.

### input

```python
X @ model[0].weight.T + model[0].bias
```

### output

```text
tensor([[-1.3198,  0.0218,  0.7287],
        [-1.1588,  0.1368, -0.2737],
        [-3.5191,  0.6868,  0.7409],
        [-3.3581,  0.8019, -0.2615]], grad_fn=<AddBackward0>)
```

## Optimizer

옵티마이저는 모델을 등록하여 해당 모델의 파라미터들을 grad에 맞춰 학습시켜주는 객체입니다.

역할을 나누면

1. loss가 자신에 등록된 수식을 이용해 미분값을 `Parameter.grad`에 더해줌
2. optimizer가 Parameters에 대해서 학습률을 적용한 각각의 grad를 적용해줌

과 같이 이루어집니다.

### input

```python
optimizer = torch.optim.SGD(
    model.parameters(),
    lr=0.01
)
```

## optimizer.param_groups

`param_groups` 속성을 이용하여 내부에 존재하느 파라미터와 메타 속성을 확인할 수 있습니다.

### input

```python
optimizer.param_groups
```

### output

```text
[{'params': [Parameter containing:
   tensor([[-0.4693, -0.6303],
           [ 0.2238,  0.1087],
           [-0.4982,  0.5043]], requires_grad=True),
   Parameter containing:
   tensor([ 0.4101, -0.4195,  0.2183], requires_grad=True),
   Parameter containing:
   tensor([[ 0.2860,  0.3570, -0.5004]], requires_grad=True),
   Parameter containing:
   tensor([-0.5282], requires_grad=True)],
  'lr': 0.01,
  'momentum': 0,
  'dampening': 0,
  'weight_decay': 0,
  'nesterov': False,
  'maximize': False,
  'foreach': None,
  'differentiable': False,
  'fused': None}]
```

## 학습 전 Parameter 저장

학습 이후의 상태를 비교하기 위해 `.clone()`를 통해 가중치 및 절편을 저장하겠습니다.

`detach()`는 실제 Tensor 값을 별도로 복사함을 의미합니다. 이는 곧 Tensor을 autograd 계산에 그래프에서 뗴어냄을 의미합니다.

### input

```python
before_train = {
    "w1": model[0].weight.detach().clone(),
    "b1": model[0].bias.detach().clone(),
    "w2": model[2].weight.detach().clone(),
    "b2": model[2].bias.detach().clone(),
}

before_train
```

### output

```text
{'w1': tensor([[-0.4693, -0.6303],
         [ 0.2238,  0.1087],
         [-0.4982,  0.5043]]),
 'b1': tensor([ 0.4101, -0.4195,  0.2183]),
 'w2': tensor([[ 0.2860,  0.3570, -0.5004]]),
 'b2': tensor([-0.5282])}
```

## 학습 1번 실행해주기

optimizer에 등록되어있는 모든 `Parameter.grad`를 0으로 초기화해줍니다.

```python
optimizer.zero_grad()
```

바로 예측 해주며 그래프를 만들어줍니다.

```python
y_pred = model(X)
```

만들어진 그래프를 다시 loss_fn으로 손실함수 그래프까지 추가해주고 계산해줍니다.

```python
loss = loss_fn(y_pred, y)
```

그래프를 타고 올라가서 모든 학습 대상에 대하여 `Parameter.grad += new_grad` 해줍니다.

```python
loss.backward()
```

모델에 존재하는 파라미터의 기울기 값을 확인해줍니다.

### input

```python
for name, param in model.named_parameters():
    print(f"{name} grad:", param.grad)
    print()
```

### output

```text
0.weight grad: tensor([[  0.0000,   0.0000],
        [-11.2061, -11.3520],
        [  6.7165,   9.6033]])

0.bias grad: tensor([ 0.0000, -3.9738,  2.8868])

2.weight grad: tensor([[ 0.0000, -5.8122, -4.2510]])

2.bias grad: tensor([-11.1300])
```

결과적으로 1번 뉴런은 계속 dead 상태임을 확인할 수있으며 각각 가중치를 받은 상태임을 확인할 수 있습니다.

`0.weight`의 grad와 `2.weight`의 grad의 shape는 각각 `[3, 2]`, `[1. 3]` 으로 각각 전치하면 `[2, 3]`, `[3, 1]` 이 되어 결국 `3 -> 1` 의 형태가 되는것을 알 수 있습니다.

## optimizer.step()

이제 학습되어져있는 `Parameter.grad`를 이용하여 실제 Parameter의 값을 바꾸겠습니다.

```python
optimizer.step()
```

## 학습 전후 Parameter 비교

weight, bias가 `before_train`과 비교하여 바뀐것을 확인할 수 있습니다.

주목할점은 첫번재 뉴런은 변화가 존재하지 않는다는 점입니다.

### input

```python
print()

for (k, v), (name, param) in zip(before_train.items(), model.named_parameters()):
    print(f"before {k}:\n", v)
    print(f"\nafter {name}:\n", param)

    print("\n\n")
```

### output

```text
before w1:
 tensor([[-0.4693, -0.6303],
        [ 0.2238,  0.1087],
        [-0.4982,  0.5043]])

after 0.weight:
 Parameter containing:
tensor([[-0.4693, -0.6303],
        [ 0.3358,  0.2223],
        [-0.5654,  0.4083]], requires_grad=True)



before b1:
 tensor([ 0.4101, -0.4195,  0.2183])

after 0.bias:
 Parameter containing:
tensor([ 0.4101, -0.3797,  0.1895], requires_grad=True)



before w2:
 tensor([[ 0.2860,  0.3570, -0.5004]])

after 2.weight:
 Parameter containing:
tensor([[ 0.2860,  0.4152, -0.4579]], requires_grad=True)



before b2:
 tensor([-0.5282])

after 2.bias:
 Parameter containing:
tensor([-0.4169], requires_grad=True)
```

# 마무리
이번에는 `PyTorch`의 라이브러리를 천천히 뜯어보는 시간을 가졌습니다.

아무래도 처음 접하여 클론코딩을 하였을 때는 잘 이해되지 않았던 부분이 여유를 가지고 클래스, 메서드, 속성 등을 찍어보며 해보니 이해가 잘 되었던 것 같습니다. (이전 포스팅에 올렸듯 수학을 공부한 것도 한몫 한 것 같습니다.)

이후에는 조금 확장하여 여러 모델 또는 자동으로 여러 `epoch`를 돌리며 모델을 학습시키는 방향, 그리고 학습 과정을 추적하는 작업에 익숙해져보도록 하겠습니다.

