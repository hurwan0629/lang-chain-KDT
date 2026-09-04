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
        """인자로 num_classes를 받아서 우리가 원하는만큼 정리할 수 있게 만들어보기"""
        super().__init__()

        # 마지막 레이어 빼고 프리징 시킬지 결정
        self.freeze_features = freeze_features

        # backbone = 특징을 뽑아내는 본체
        self.backbone = densenet121(
            weights=DenseNet121_Weights.DEFAULT
        )

        # freeze_features가 존재한다면 일단 파라미터를 모두 고정시켜주기 (
        # freeze_features가 False여도 backbone은 그대로 사용하지만 학습에 포함되게 됨
        if self.freeze_features:
            for parameter in self.backbone.features.parameters():
                parameter.requires_grad = False

        # DenseNet의 마지막 모듈로 등록되어있는 classifier 모듈에서 infeatures를 뽑아서
        # 이를 우리 프로젝트의 마지막 레이어로 변환할 준비를 해주기
        in_features = self.backbone.classifier.in_features  # DenseNet121: 1024

        self.backbone.classifier = nn.Linear(
            in_features,
            num_classes,
        )

    # backbone = densenet121 모델
    def forward(self, x):
        return self.backbone(x)


    def train(self, mode: bool = True):
        """
        train()은 내부적으로 각 모듈에 대한 상태를 바꾸는 것을 말합니다.
        기본적으로 nn.Module에는 training 상태가 존재하며 이를 재귀적으로 상태를 전파해주게 됩니다.

        이때 densenet121() 객체의 BatchNorm, Dropout까지 고정시키기 위해서 해당 메서드를
        오버라이딩하였습니다.
        """
        super().train(mode)

        # mode가 train이며 freeze_features가 켜져있다면
        if mode and self.freeze_features:
            # 모든 피처들을 eval로 변형해주기
            self.backbone.features.eval()

        return self


def create_model(num_classes: int, freeze_features: bool = True):
    """해당 함수는 새로운 num_classes 개수 만큼의 FaceDenseNet121 모델을 반환하게 됩니다."""
    return FaceDenseNet121(
        num_classes=num_classes,
        freeze_features=freeze_features,
    )


def count_parameters(model: nn.Module):
    """모델을 넣으면 Parameter에 대한 (total, trainable) 을 반환하게 됩니다."""
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(
        p.numel()
        for p in model.parameters()
        if p.requires_grad
    )

    return total, trainable


def load_model_state(model: nn.Module, checkpoint_file, device):
    """저장되어있는 .pth 파일에 대해서 state_dict를 받아오게 됩니다."""
    checkpoint = torch.load(
        checkpoint_file,
        map_location=device,
    )

    # checkpoint = { "model_state_dict": ... } 과 같이 저장되어있음을 기대합니다.
    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    return checkpoint


if __name__ == "__main__":
    # 모델을 하나 만든뒤
    model = create_model(num_classes=3)

    # 파라미터 개수를 한번 확인하게 됩니다.
    # FreezeFeatures=True 일 경우에는 반환 값은 (전체 개수: 6,956,931, (1024+1)*3) 입니다.
    total, trainable = count_parameters(model)

    print(model.backbone.classifier)
    print(f"전체 parameter: {total:,}")
    print(f"학습 parameter: {trainable:,}")
