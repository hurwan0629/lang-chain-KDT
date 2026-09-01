import torch
from torch import nn
from torchvision.models import densenet121, DenseNet121_Weights


class FaceDenseNet121(nn.Module):
    """
    ImageNet pretrained DenseNet121을 얼굴 분류기로 전이학습한다.

    기본 전략:
    DenseNet의 feature extractor는 freeze하고,
    마지막 classifier만 현재 사람 수에 맞게 새로 학습한다.
    """

    def __init__(self, num_classes: int, freeze_features: bool = True):
        super().__init__()

        self.freeze_features = freeze_features

        self.backbone = densenet121(
            weights=DenseNet121_Weights.DEFAULT
        )

        if self.freeze_features:
            for parameter in self.backbone.features.parameters():
                parameter.requires_grad = False

        in_features = self.backbone.classifier.in_features  # DenseNet121: 1024

        self.backbone.classifier = nn.Linear(
            in_features,
            num_classes,
        )

    def forward(self, x):
        return self.backbone(x)

    def train(self, mode: bool = True):
        """
        features를 freeze한 상태라면 BatchNorm의 running_mean/running_var까지
        학습 중 바뀌지 않도록 feature extractor는 eval 상태로 유지한다.
        """
        super().train(mode)

        if mode and self.freeze_features:
            self.backbone.features.eval()

        return self


def create_model(num_classes: int, freeze_features: bool = True):
    return FaceDenseNet121(
        num_classes=num_classes,
        freeze_features=freeze_features,
    )


def count_parameters(model: nn.Module):
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    return total, trainable


def load_model_state(model: nn.Module, checkpoint_file, device):
    checkpoint = torch.load(
        checkpoint_file,
        map_location=device,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    return checkpoint


if __name__ == "__main__":
    model = create_model(num_classes=3)

    total, trainable = count_parameters(model)

    print(model.backbone.classifier)
    print(f"전체 parameter: {total:,}")
    print(f"학습 parameter: {trainable:,}")
