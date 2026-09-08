import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()

        self.features = nn.Sequential(
            # Block 2
            # feature map을 늘려 기본적인 특징을 잡아주며
            # 연산량을 많이 잡아먹는 image size를 줄여줌
            # Conv (b, 3, 32, 32)
            nn.Conv2d(3, 32, (3, 3), 1, 1),
            # BN    (b, 32, 32, 32)
            nn.BatchNorm2d(32),
            # ReLU
            nn.ReLU(inplace=False),
            # Pool (b, 32, 32, 32)
            nn.MaxPool2d(2),

            # Block 1
            # 일반적으로 여기에서 32 -> 32를 조금 더 해서 기본적인 특징을 좀 더 상세하게 잡아주기도 하는데
            # 여기에서는 작은 모델이기 떄문에 이를 조금 더 빠르게 채널을 늘리는 방식
            # Conv (b, 32, 16, 16)
            nn.Conv2d(32, 64, (3, 3), 1, 1),
            # BN    (b, 64, 16, 16)
            # 채널에 대해서 정규화를 하여 연산 범위를 지속적으로 조절해줌
            # 이를 통해서 연산 범위를 지속적으로 일정하게 잡을 수 있음
            nn.BatchNorm2d(64),
            # ReLU (b, 64, 16, 16)
            # 활성화함수
            nn.ReLU(inplace=False),
            # Pool
            # 다시 한번 잡아주기
            nn.MaxPool2d(2, stride=2)
            # (b, 64, 16, 16)
        )

        self.classifier = nn.Sequential(
            # 먼저 (b, 64*8*8)으로 shape 줄여주기
            nn.Flatten(),
            # 그리고 Linear을 이용해서 빠르게 좁혀주기
            # 굉장히 빠르다고 생각이 들기는 함
            nn.Linear(2**12, 128),
            # 활성화 함수로 음수 값 한번 잡아주기
            nn.ReLU(),
            # Dropout을 이용해서 확률적으로 FC 레이어 퍼셉트론들을 꺼주고
            # 10/7을 곱하여 배율 먹여줘서 기댓값 그대로 만들기
            nn.Dropout(p=0.3),
            # 최종적으로 10개의 logits를 만들어주기
            nn.Linear(128, 10)
        )


    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)