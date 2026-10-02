"""
1997년 Hochreiter & Schmidhuber의 원 논문을 기준으로 만든 학습용 LSTM 구현.

중요:
- torch.nn.LSTM을 사용하지 않고, 논문의 memory cell 식을 직접 구현한다.
- 1997 원형 LSTM에는 forget gate가 없다.
- CEC(Constant Error Carousel)의 self-connection 계수는 고정 1.0이다.
- 논문의 truncated error-flow 아이디어를 보기 위해, 기본값으로
  gate/candidate 쪽 recurrent 경로의 "시간을 거슬러가는 gradient"는 끊고
  cell state s_t -> s_(t-1) 경로만 길게 유지한다.

논문 핵심 식(메모리 셀 하나를 벡터화한 형태):

    i_t = sigmoid(net_i(t))                 # input gate
    o_t = sigmoid(net_o(t))                 # output gate

    g(x) = 4 * sigmoid(x) - 2              # 논문 실험의 g: [-2, 2]
    h(x) = 2 * sigmoid(x) - 1              # 논문 실험의 h: [-1, 1]

    s_t = s_(t-1) + i_t * g(net_c(t))      # CEC: 이전 state가 계수 1로 전달
    y_t = o_t * h(s_t)                     # memory cell의 출력

여기서
- s_t: internal state, 즉 cell memory
- y_t: 밖으로 보이는 memory cell output
- W/U/b: 학습되는 파라미터
- s_(t-1) -> s_t의 '+ s_(t-1)' 연결: 학습되는 weight가 아니라 고정 계수 1
"""

from __future__ import annotations

import torch
from torch import Tensor, nn
import torch.nn.functional as F


def paper_g(x: Tensor) -> Tensor:
    """1997 논문 실험에서 사용한 g(x): 출력 범위 [-2, 2]."""
    return 4.0 * torch.sigmoid(x) - 2.0


def paper_h(x: Tensor) -> Tensor:
    """1997 논문 실험에서 사용한 h(x): 출력 범위 [-1, 1]."""
    return 2.0 * torch.sigmoid(x) - 1.0


class LSTM1997Cell(nn.Module):
    """
    1997 LSTM의 memory cell을 벡터 단위로 구현.

    여기서는 논문의 자유로운 network topology 중 이해하기 쉬운 형태를 택한다.

        현재 입력 x_t
        이전 memory-cell output y_(t-1)

    두 값이 input gate, output gate, cell input(candidate)를 만든다.

    논문 자체는 gate unit / 다른 memory cell / conventional hidden unit 등
    더 많은 unit을 recurrent input으로 연결하는 것도 허용한다.
    """

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        *,
        paper_truncated_gradient: bool = True,
    ) -> None:
        super().__init__()

        # x 크기
        self.input_size = input_size
        # h 벡터 크기
        self.hidden_size = hidden_size
        # 
        self.paper_truncated_gradient = paper_truncated_gradient

        # ------------------------------------------------------------
        # 1) Input gate
        #
        # net_i(t) = W_i x_t + U_i y_(t-1) + b_i
        # i_t      = sigmoid(net_i(t))
        #
        # i_t는 "이번 입력을 cell memory 안에 얼마나 기록할지" 정한다.
        # ------------------------------------------------------------
        self.W_i = nn.Parameter(torch.empty(hidden_size, input_size))
        self.U_i = nn.Parameter(torch.empty(hidden_size, hidden_size))
        self.b_i = nn.Parameter(torch.zeros(hidden_size))

        # ------------------------------------------------------------
        # 2) Output gate
        #
        # net_o(t) = W_o x_t + U_o y_(t-1) + b_o
        # o_t      = sigmoid(net_o(t))
        #
        # o_t는 "cell memory를 밖으로 얼마나 보여줄지" 정한다.
        # ------------------------------------------------------------
        self.W_o = nn.Parameter(torch.empty(hidden_size, input_size))
        self.U_o = nn.Parameter(torch.empty(hidden_size, hidden_size))
        self.b_o = nn.Parameter(torch.zeros(hidden_size))

        # ------------------------------------------------------------
        # 3) Cell input
        #
        # net_c(t) = W_c x_t + U_c y_(t-1) + b_c
        # g_t      = g(net_c(t))
        #
        # g_t는 cell에 새로 기록하려는 내용(candidate)이다.
        # ------------------------------------------------------------
        self.W_c = nn.Parameter(torch.empty(hidden_size, input_size))
        self.U_c = nn.Parameter(torch.empty(hidden_size, hidden_size))
        self.b_c = nn.Parameter(torch.zeros(hidden_size))

        self.reset_parameters()

    def reset_parameters(self) -> None:
        """
        학습용으로 작은 값으로 초기화한다.

        원 논문은 실험마다 초기화 조건/게이트 bias가 조금씩 다르므로
        여기서는 특정 실험의 초기값을 복제하기보다 구조 자체에 집중한다.
        """
        for weight in (
            self.W_i,
            self.U_i,
            self.W_o,
            self.U_o,
            self.W_c,
            self.U_c,
        ):
            nn.init.uniform_(weight, -0.1, 0.1)

        nn.init.zeros_(self.b_i)
        nn.init.zeros_(self.b_o)
        nn.init.zeros_(self.b_c)

    def forward(
        self,
        x_t: Tensor,
        y_prev: Tensor,
        s_prev: Tensor,
    ) -> tuple[Tensor, Tensor, dict[str, Tensor]]:
        """
        한 timestep의 forward.

        Args:
            x_t:
                현재 입력.
                shape = [batch, input_size]

            y_prev:
                이전 timestep의 memory-cell output.
                shape = [batch, hidden_size]

            s_prev:
                이전 timestep의 internal state / cell memory.
                shape = [batch, hidden_size]

        Returns:
            y_t:
                현재 memory-cell output.

            s_t:
                현재 internal state / cell memory.

            cache:
                공부할 때 각 gate와 중간값을 직접 볼 수 있도록 반환.
        """

        # ------------------------------------------------------------
        # 논문 학습 알고리즘의 핵심적인 "truncation"을 흉내낸다.
        #
        # 1997 논문에서는 net_i, net_o, net_c에 도달한 error가
        # 그 연결을 타고 계속 과거로 전파되지는 않게 한다.
        #
        # 따라서 recurrent gate/candidate 계산에는 y_prev.detach()를 넣는다.
        #
        # 중요한 점:
        # - U_i/U_o/U_c의 gradient는 여전히 계산된다.
        # - 단지 이 경로를 통해 y_prev보다 더 과거로 gradient가 가지 않는다.
        # - s_prev -> s_t의 CEC 경로는 detach하지 않는다.
        # ------------------------------------------------------------
        recurrent_source = (
            y_prev.detach()
            if self.paper_truncated_gradient
            else y_prev
        )

        # input gate
        net_i = (
            F.linear(x_t, self.W_i)
            + F.linear(recurrent_source, self.U_i)
            + self.b_i
        )
        i_t = torch.sigmoid(net_i)

        # output gate
        net_o = (
            F.linear(x_t, self.W_o)
            + F.linear(recurrent_source, self.U_o)
            + self.b_o
        )
        o_t = torch.sigmoid(net_o)

        # 새로 cell에 넣을 정보
        net_c = (
            F.linear(x_t, self.W_c)
            + F.linear(recurrent_source, self.U_c)
            + self.b_c
        )
        g_t = paper_g(net_c)

        # ============================================================
        # CEC (Constant Error Carousel)
        #
        # 논문:
        #   s_t = s_(t-1) + i_t * g(net_c(t))
        #
        # 여기서 s_prev 앞에는 학습되는 weight가 없다.
        # "고정된 1.0 self-connection"이므로:
        #
        #   d s_t / d s_(t-1) = 1
        #
        # 이 직접 경로를 통해 error가 여러 timestep을 지나도
        # 반복해서 1을 곱하며 전달될 수 있다.
        # ============================================================
        s_t = s_prev + i_t * g_t

        # memory cell output
        #
        # 논문:
        #   y_c(t) = y_out(t) * h(s_c(t))
        #
        # cell 안에 저장된 s_t 자체와,
        # 밖으로 노출되는 y_t를 반드시 구분해서 보자.
        h_s = paper_h(s_t)
        y_t = o_t * h_s

        cache = {
            "net_i": net_i,
            "input_gate": i_t,
            "net_o": net_o,
            "output_gate": o_t,
            "net_c": net_c,
            "candidate_g": g_t,
            "state_s": s_t,
            "scaled_state_h": h_s,
            "cell_output_y": y_t,
        }

        return y_t, s_t, cache


class LSTM1997(nn.Module):
    """
    LSTM1997Cell을 sequence 전체에 반복 적용하는 얇은 wrapper.

    입력 shape:
        [sequence, batch, input_size]

    반환:
        y_seq: [sequence, batch, hidden_size]
        s_seq: [sequence, batch, hidden_size]
        traces: timestep별 gate / candidate / state 값

    학습용 구현이라 output projection은 일부러 넣지 않았다.
    즉 여기서 y_t는 "memory cell output"이고,
    실제 분류/회귀를 하려면 바깥에 nn.Linear 등을 붙이면 된다.
    """

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        *,
        paper_truncated_gradient: bool = True,
    ) -> None:
        super().__init__()

        self.hidden_size = hidden_size
        self.cell = LSTM1997Cell(
            input_size=input_size,
            hidden_size=hidden_size,
            paper_truncated_gradient=paper_truncated_gradient,
        )

    def forward(
        self,
        x: Tensor,
        *,
        y0: Tensor | None = None,
        s0: Tensor | None = None,
    ) -> tuple[Tensor, Tensor, list[dict[str, Tensor]]]:
        if x.ndim != 3:
            raise ValueError(
                "x는 [sequence, batch, input_size] 형태여야 합니다."
            )

        seq_len, batch_size, _ = x.shape

        if y0 is None:
            y_prev = x.new_zeros(batch_size, self.hidden_size)
        else:
            y_prev = y0

        if s0 is None:
            # 논문의 s_c(0) = 0
            s_prev = x.new_zeros(batch_size, self.hidden_size)
        else:
            s_prev = s0

        outputs: list[Tensor] = []
        states: list[Tensor] = []
        traces: list[dict[str, Tensor]] = []

        for t in range(seq_len):
            y_t, s_t, cache = self.cell(
                x_t=x[t],
                y_prev=y_prev,
                s_prev=s_prev,
            )

            outputs.append(y_t)
            states.append(s_t)
            traces.append(cache)

            # 다음 timestep으로 넘겨주는 두 종류의 값:
            # y_t -> 외부에서 보이는 recurrent output
            # s_t -> CEC 내부 memory
            y_prev = y_t
            s_prev = s_t

        y_seq = torch.stack(outputs, dim=0)
        s_seq = torch.stack(states, dim=0)

        return y_seq, s_seq, traces
