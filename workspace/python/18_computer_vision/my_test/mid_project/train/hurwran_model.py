from torch import nn

from my_test.mid_project.train.class_model import ShapeCNN
from my_test.mid_project.train.env import CHECKPOINT_FILE

class HurwanBaseModel(nn.Module):
    def __init__(self, num_classes=3):
        """모델은 (3, 224, 224) 모델을 기대함"""
        super().__init__()

        self.features = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # (b, 32, 112, 112)

            nn.Conv2d(in_channels=32, out_channels=32, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            # (b, 32, 112, 112)

            nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            # (b, 64, 112, 112)

            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # (b, 64, 56, 56)

            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2),
            # (b, 64, 28, 28)

            nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, padding=1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True)
            # (b, 64, 28, 28)
        )

        self.avgpool = nn.AdaptiveAvgPool2d((4, 4))
        # (b, 64, 4, 4)

        self.fc_classifier = nn.Sequential(
            nn.Flatten(start_dim=1),

            nn.Dropout(p=0.5),
            nn.Linear(64*4*4, 2**8),
            nn.ReLU(inplace=True),

            nn.Dropout(p=0.5),
            nn.Linear(2**8, 2**6),
            nn.ReLU(inplace=True),

            nn.Linear(2**6, num_classes)
        )

    def forward(self, x):
        x = self.features(x)

        x = self.avgpool(x)

        return self.fc_classifier(x)