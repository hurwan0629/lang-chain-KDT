# DenseNet121 얼굴 분류 빠른 적용

## 예상 폴더 구조

```text
mid_project/
├─ dataset/
│  ├─ train/
│  │  ├─ person_a/
│  │  │  ├─ 001.jpg
│  │  │  └─ ...
│  │  ├─ person_b/
│  │  └─ person_c/
│  │
│  └─ test/
│     ├─ person_a/
│     ├─ person_b/
│     └─ person_c/
│
├─ models/
│
└─ train/
   ├─ __init__.py
   ├─ env.py
   ├─ transforms.py
   ├─ dataset.py
   ├─ model.py
   ├─ train.py
   ├─ evaluate.py
   └─ inference.py
```

## 실행 순서

데이터/Loader 확인:

```bash
python train/dataset.py
```

학습:

```bash
python train/train.py
```

최종 test 평가:

```bash
python train/evaluate.py
```

## 학습 흐름

```text
ImageFolder
→ train/validation split
→ DataLoader
→ ImageNet pretrained DenseNet121
→ features freeze
→ classifier Linear(1024, 사람 수)
→ CrossEntropyLoss
→ AdamW
→ ReduceLROnPlateau
→ validation loss 기준 best checkpoint 저장
```

## OpenCV와 연결

```python
from train.inference import (
    load_face_classifier,
    predict_face_bgr,
)

model, idx_to_class = load_face_classifier()

# face_crop은 OpenCV에서 검출해서 자른 BGR ndarray
name, confidence = predict_face_bgr(
    face_crop,
    model,
    idx_to_class,
)
```

학습과 실시간 추론 모두 같은 `test_transform`의
Resize / ToTensor / ImageNet Normalize 규격을 사용한다.
