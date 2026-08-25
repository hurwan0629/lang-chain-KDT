# [머신러닝] 수업시간에 생겼었던 질문들 정리
> 주말동안 공부한 것을 제외한 남은 궁금증을 해결한 글입니다.
## 1. Adam과 AdamW
Adam은 각 Parameter마다 gradient의 통계를 기억하면서 학습률을 조절하는 Optimizer입니다.

이는 형태가 가중치에 새로 만들어진 기울기에 학습률을 적용한 값을 넣습니다.

이때 Adam은 gradient의 이동 평균과 $\operatorname{gradient}^2$를 함꼐 저장합니다.

이는 다음과 같은 식으로 설명이 됩니다.

방향 ($\beta$는 기억하는 정도. `0`이 기억 안함, `1`에 가까울수록 오래 기억함):

$$
m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t
$$

크기 (방향을 무시하기 위해 제곱): 

$$
v_t = \beta_2 v_{t-1} + (1-\beta_2)g^2_t
$$

최종 가중치 (크기가 방향에 비해 계속 커지면 학습 폭이 저절로 줄여지게 됩니다. 반대로 기울기가 계속 작아지면 학습폭이 더 커질 수 있습니다.)

$$
w = w - \eta \frac{\hat{m}}{\sqrt{\hat{v} + \epsilon}}
$$

이를 통해서 기울기가 어떤 방향으로 계속 가고있는지와 그 크기의 방향에 따라 실질적인 update 크기를 조절하게 됩니다.

**AdamW**의 경우에는 `weight decay`를 Adam의 gradient 계산에서 분리했다는 것입니다.

AdamW에서는 크게
1. weight decay로 w 자체를 조금 줄이며
2. Adam 방식으로 gradient update를 하게 됩니다.

따라서 먼저 $w = w - \eta \lambda w $ 가 일어난 뒤 Adam update가 적용되게 됩니다.

weight decay란 가중치를 학습시킬 때 학습 데이터에 대해서 과적합이 일어나지 않게 학습 시점에 weight를 일부 깎아내는 기법을 말합니다.

이는 다음과 같이 표현이 가능합니다.

$$
w = w - \eta \operatorname{gradient} - \eta \lambda w
$$

## 2. 퍼셉트론
가장 기본적인 인공 뉴런 모델로 선형 변환 이후 활성화 함수를 거치는 것과 같은 레이어 계층을 말합니다.

## 3. view()
Tensor()의 메서드중 `Tensor.view(shape)` 형태로 생성 가능한 뷰 객체입니다.

이는 새 데이터를 복사하는 것이 아닌 원본을 다른 shape로 바라보는 형태입니다.

## 4. DNN
DNN은 Deep Neural Network의 약자로 hidden layer을 여러층 쌓은 Neural Network라는 넓은 표현을 말합니다.

## 5. 옵티마이저의 정확한 정의
gradient와 자신의 내부 상태를 이용하여 학습 가능한 파라미터를 어떤 규칙으로 갱신할지를 정의해놓은 알고리즘 및 객체 입니다.

## 6. Sheduler
Scheduler은 Optimizer의 learning rate를 시간에 따라 조절하는 객체로 학습률, loss 상태, 모멘텀 등에 따라 학습률 (`lr`)을 조절해주는 것을 말합니다.