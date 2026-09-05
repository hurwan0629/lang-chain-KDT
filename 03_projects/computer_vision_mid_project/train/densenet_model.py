from torchvision.models import densenet121, DenseNet121_Weights

"""
[2026-09-01 20:06:27]

hurwan_model.py 이후 densenet를 타겟으로 한번 전이학습 해보기로 결정 
"""

model = densenet121(
    weights=DenseNet121_Weights.DEFAULT
)

# print(model)
print(model.classifier)

