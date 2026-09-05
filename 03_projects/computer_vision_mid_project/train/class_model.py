import torch.nn as nn

class ShapeCNN(nn.Module):
    def __init__(self, num_classes=3):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            # 좋은 모델들은 어느정도 레이어를 n개로 나눠서 쓰기도 함(Conv 1 -> 64 보다는 1 -> 32, 32 -> 32 형태)
            nn.Conv2d(32, 32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            # inplace = 덮어쓰기 옵션 (기존 텐서값을 직접 변경하라는 뜻)
            # BatchNorm에서 넘어온 Tensor을 별도의 새로운 Tensor로 복사해서 처리하지 않고
            # Tensor의 메모리를 직접 수정하여 모리를 절약
            nn.ReLU(inplace=True),
            # 특징 추출하기
            nn.MaxPool2d(kernel_size=2),

            nn.Conv2d(32, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            # 좋은 모델들은 어느정도 레이어를 n개로 나눠서 쓰기도 함(Conv 1 -> 64 보다는 1 -> 32, 32 -> 32 형태)
            nn.Conv2d(64, 64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            # inplace = 덮어쓰기 옵션 (기존 텐서값을 직접 변경하라는 뜻)
            # BatchNorm에서 넘어온 Tensor을 별도의 새로운 Tensor로 복사해서 처리하지 않고
            # Tensor의 메모리를 직접 수정하여 모리를 절약
            nn.ReLU(inplace=True),
            # 특징 추출하기
            nn.MaxPool2d(kernel_size=2),
        )

        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Dropout(p=0.25),
            nn.Linear(64*1*1, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        return self.classifier(x)