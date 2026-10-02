"""
RNN -> BPTT -> LSTM을 직접 코드로 확인하는 학습용 파일.

진행 순서
1. Vanilla RNN forward
2. timestep을 펼쳐서 hidden state 변화 확인
3. BPTT / Jacobian
4. gradient vanishing / exploding
5. 1997 LSTM의 CEC
6. 현대 LSTM과 비교
"""

import numpy as np


# 우선 첫 단계에서 쓸 아주 작은 Vanilla RNN 예제
input_size = 2
hidden_size = 3

# input sequence [3, 2]
W_xh = np.array([
    [0.2, -0.1],
    [0.4,  0.3],
    [-0.5, 0.2],
])

# hidden state [3, 3]
W_hh = np.array([
    [0.5, 0.1, 0.0],
    [0.0, 0.4, 0.2],
    [0.1, 0.0, 0.3],
])

b_h = np.zeros(hidden_size)


def rnn_step(x_t, h_prev):
    """
    h_t = tanh(W_xh @ x_t + W_hh @ h_{t-1} + b_h)

    net_t:
        활성화 함수에 들어가기 전 값

    h_t:
        현재 timestep의 hidden state
    """
    # W_xh: [d_k, ]
    net_t = W_xh @ x_t + W_hh @ h_prev + b_h
    h_t = np.tanh(net_t)
    return net_t, h_t


if __name__ == "__main__":
    x_t = np.array([1.0, 0.5])
    h_prev = np.zeros(hidden_size)

    net_t, h_t = rnn_step(x_t, h_prev)

    print("net_t =", net_t)
    print("h_t   =", h_t)
