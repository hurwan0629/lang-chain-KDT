from torchvision import transforms

try:
    from .env import IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD
except ImportError:
    from env import IMAGE_SIZE, IMAGENET_MEAN, IMAGENET_STD


# 얼굴이 이미 어느 정도 crop되어 들어온다는 전제.
# RandomResizedCrop 기본 scale=(0.08, 1.0)은 얼굴을 지나치게 잘라낼 수 있어
# 얼굴 데이터에 맞게 범위를 좁혀둠.
train_transform = transforms.Compose([
    # 랜덤으로 리사이징 해준 뒤 crop까지 해줌
    transforms.RandomResizedCrop(
        (IMAGE_SIZE, IMAGE_SIZE),   # 최종 출력 크기
        scale=(0.8, 1.0),      # 원본 이미지에서 0.8 ~ 1.0 사용
        ratio=(0.9, 1.1),       # crop 영역의 가로/세로 비율을 0.9~1.1로 제한
    ),      # 마지막에 IMAGE_SIZE (보통 224)로 조절해서 반환
    # 랜덤 flip 시켜주기
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(
        brightness=0.2,     # 명암    약 ~20%
        contrast=0.2,       # 대비    약 ~20%
        saturation=0.2,     # 채도    약 ~20%
        hue=0.05,           # 색상 자체 이동
    ),
    # 아핀 변환해주기
    transforms.RandomAffine(
        degrees=15, # 각도
        translate=(0.1, 0.1),    # 10% 이동
        scale=(0.9, 1.1),   # 크기 변환
        shear=5,     # 평행 변환
    ),
    # MINMAX 표준화 + 텐서형으로 정리
    transforms.ToTensor(),
    transforms.Normalize(
        mean=IMAGENET_MEAN,
        std=IMAGENET_STD,
    ),
])


# 평가/실시간 추론에서는 랜덤 변환을 사용하지 않음.
test_transform = transforms.Compose([
    transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=IMAGENET_MEAN,
        std=IMAGENET_STD,
    ),
])
