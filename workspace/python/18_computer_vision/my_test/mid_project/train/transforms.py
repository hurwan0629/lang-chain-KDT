from torchvision import transforms

"""
어떤 이미지든 (640 x 480 (W, H)) 
"""


"""
2026-09-01 18:42:25
[transforms 설계]
우선 카메라에서 받는 이미지의 크기는 640x480 이지만 학습용 모델의 크기는 다를 수 있습니다.

이를 해결하기 위해 
- train_transform에서는 RandomResizedCrop를 사용하며
- test_transform에서는 resize를 사용할 예정입니다.

추가적으로 데이터 학습을 위해 train에는 이런저런 증강을 너무 심하지 않은 범위에서 적용할 
생각이며, test에서는 Resize와 CenterCrop + ToTensor 등 정도만 적용할 생각입니다.

train할때 사용할 transforms로는
- RandomHorizontalFlip(p=0.5): 좌우와 상관없이 얼굴의 특징만을 잘 뽑기 위해
- RandomRotation(degrees=30): 실제로 고개를 까닥일 수 있는데 그 범위가 -30 ~ 30 정도라고 생각이 들어서
- RandomAffine 
"""
train_transform = transforms.Compose([
    transforms.RandomResizedCrop((224, 224)),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(
        brightness=0.2,     # 밝기 변화: -20% ~ 20%
        contrast=0.2,       # 대비 변화: -20% ~ 20%
        saturation=0.2,     # 채도 변화: -20% ~ 20%
        hue=0.05            # 색상 변화
    ),
    transforms.RandomAffine(
        degrees=30,             # 회전
        translate=(0.1, 0.1),   # 가로 세로 최대 10%
        scale=(0.9, 1.1),       # 90% ~ 110% 확대/축소
        shear=5                 # 기욱이기 (이미지 자체를)
    ),
    transforms.ToTensor(),
    # transforms.Normalize(mean= ,std=)
])

test_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor()
    # transforms.Normalize(mean= ,std=)
])