# [머신러닝] 규제
> 이번에는 규제에 대해서 글을 작성해보겠습니다.

이번에 $\operatorname{AdamW}$를  알아보던 중 $\operatorname{Weight\,decay}$ 또한 규제 방식이라는 점을 알고 규제가 그냥 레이어에서만 일어나는 것이 아니구나 하고 알게되어서 조금 더 알아보고자 글을 작성합니다.

## 규제가 무엇인가
규제의 의미는 다음과 같습니다.

> 모델이 학습 데이터에 지나치게 맞춰지는 것을 막고, 더 일반화 되는 해를 선택하도록 학습에 제약이나 편향을 주는 모든 방법

여기에서 제가 이전에 알던 규제는 $L1$, $L2$ 규제를 말했습니다.

이는 모두 손실함수에 규제식을 추가하여 구현하는 방식입니다. ($L1$은 릿지(절대평균), $L2$는 라쏘(제곱 평균)을 말합니다.)

여기에서 $L2$ 규제가 보통 미분에 쉬운 형태를 제공하기 상대적으로 많이 사용됩니다.

$$
L_{1.Lasso} = L(w) + \lambda \sum_i {w_i^2}
$$

$$
L_{2.Ridge} = L(w) + \lambda \sum_i |w|
$$

이를 통해 특정 가중치에 대해서 미분을 할 시에 그 가중치의 크기만큼 추가로 학습률을 가해주는 규제 방식을 말합니다.

릿지 미분:

$$
\frac{d}{dw_i} L_{2.Rigge} = \frac{d}{dw_i} L(w) + 2 \lambda w_i
$$

SGD 최적화 학습률 적용

$$
w_i = w_i - \eta \frac{\partial L_{2.Ridge}}{\partial w_i}
$$

의 형태를 가지게 됩니다.

바로 이어서 **Weight decay**를 알아보겠습니다.

## $\operatorname{Weight\,decay}$
위 수식에서 $L_{2.Ridge}$를 따로 설명하지 않고 $L$이라고 하며 $w_i$ 또한 $w$로 표현하겠습니다.

이때 최적화 수식은 다음과 같이 만들어지게 됩니다. (SGD)

$$
w = w - \eta \frac{\partial L}{\partial w}
$$

이렇게 되면 특정 $\operatorname{batch}$ 의 $Loss$가 매우 크거나 매우 작을 경우에 가중치가 지나치게 흔들릴 수 있습니다.

이는 $Adam$과 $AdamW$를 사용할 때의 $Loss$ 를 확인하여 더 직관적으로 확인할 수 있습니다.

![optimizer_compare](image.png)

### $\operatorname{Adam}$
Adam은 이전에도 포스팅으로 다루었지만 `Adaptive Moment Estimation`의 약자입니다.

Adam의 수식은 다음과 같습니다. ($\beta$=기억 비율($\beta_1$은 보통 `0.9`, $\beta_2$는 보통 `0.99`), $g$=기울기, `모멘텀`=`관성에 가까운 아이디어`)

방향 누적 - 1차 모멘텀 ($m_0=0$):

$$
m_t = \beta_1 m_{t-1} + (1-\beta_1)g_t
$$

크기 누적 - 2차 모멘텀 ($v_0=0$):

$$
v_t = \beta_2 v_{t-1} + (1-\beta_2)g^2_t
$$

> $\operatorname{Adam}$은 $\operatorname{L2}$ 규제와 함께 쓰이는 경우가 많지만 위와 같이 $g$에 손실함수 및 규제까지 포함되어 조절되게 됩니다.

Bias correction - 초기 값 보정 (초기값은 `0`인 문제 해결):

$$
\hat{m_t} = \frac{m_t}{1-\beta^t_1}
$$

$$
\hat{v_t} = \frac{v_t}{1-\beta^t_2}
$$

> 위 `Bias correction`을 이용하여 $t$가 커질수록 분모가 1에 근접하여 보정을 없애주게 됩니다.

실제 파라미터 업데이트:

$$
\theta_t = \theta_{t-1} - \eta \frac{\hat{m_t}}{\sqrt{\hat{v_t}} + \epsilon} 
$$

> $\operatorname{Adam}$은 PyTorch에서 인자로 `Parameters`, `lr`, `betas=(b_1, b_2)`, `eps`를 받을 수 있습니다.

### $\operatorname{AdamW}$
$\operatorname{AdamW}$는 $\operatorname{Adam}$의 $\operatorname{Weight\,decay}$를 분리한 optimizer입니다.

수식을 먼저 보고 가는게 좋을 것 같습니다. $$

$$
\theta = \theta - \eta \lambda \theta = (1-\eta \lambda) \theta \,\,\,\,\,(\lambda = \operatorname{Weight\,decay}, \eta = \operatorname{learning\,rate})
$$

이후에 $\operatorname{Adam}$ 업데이트를 적용하여 

$$
\theta_t = \theta - \eta \frac{\hat{m_t}}{\sqrt{\hat{v_t}} + \epsilon}
$$

이는 곧 다음과 같은 형태로 통틀어 볼 수 있습니다.

$$
\theta_t = (1-\eta \lambda)\theta - \eta \frac{\hat{m_t}}{\sqrt{\hat{v_t}}+\epsilon}
$$

와 같이 볼 수 있습니다.

### 정리
오퍼레이터의 정의는 다음과 같습니다.

> 구한 손실함수를 미분하여 구한 기울기를 이용하여 최적의 가중치 값을 구해주는 알고리즘

총 정리를 해보면 현재까지 수업에서 배운 옵티마이저는 크게 3가지로
| 알고리즘 명 | 수식 | 특징 | 상대 수렴 속도 | 계산량 |
|---|---|---|---|---|
| $\operatorname{SGD}$ | $\theta_t=\theta_{t-1}-\eta g_t$ | 현재 batch에서 계산한 gradient를 직접 사용. 단순하고 메모리 사용량이 적지만 gradient 변화가 크면 진동하거나 수렴이 느릴 수 있음 | 느린 편 | 낮음 |
| $\operatorname{Adam}$ | $\theta_t=\theta_{t-1}-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}$ | $m_t$로 gradient의 방향을, $v_t$로 gradient의 크기를 누적해 파라미터별 update 크기를 조절. L2 규제를 함께 사용하면 규제 항도 Adam의 adaptive scaling 영향을 받음 | 빠른 편 | 중간 |
| $\operatorname{AdamW}$ | $\theta_t=(1-\eta\lambda)\theta_{t-1}-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}$ | Adam의 gradient update와 weight decay를 분리하여 적용. weight decay가 $m_t,v_t$ 계산에 섞이지 않아 규제의 의미가 더 명확함 | 빠른 편 | Adam과 거의 동일 |

> 이를 바탕으로 최적화 알고리즘을 선택할 때 미분 결과의 차이가 심한 경우, 안정성, 빠른 학습 등을 원할때에는 Adam 계열을 선택할 수 있으며 계산 비용, 일반화 성능을 끌어올리고 싶은 경우에는 SGD와 Momentum 방식을 섞어서 사용할 수 있습니다. 이는 튜닝 또는 데이터에 따라 달라질 수 있는 요소가 다분하기 때문에 시각화 등을 통한 비교가 필요합니다.

# 후기
이번에는 규제라고 적고 거의 최적화 함수 등에 대해서 다루는 이야기를 하였습니다.

다음에는 직접 이를 시각화를 통한 비교를 해보도록 하겠습니다.

