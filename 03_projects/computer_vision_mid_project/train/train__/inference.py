"""
OpenCV 파트(6번)에서 바로 사용할 수 있는 추론 helper.

입력:
    OpenCV BGR 얼굴 crop ndarray

출력:
    (class_name, confidence)

주의:
    얼굴 검출 자체는 이 파일에서 하지 않는다.
    OpenCV에서 얼굴 영역을 crop한 뒤 predict_face_bgr()에 전달한다.
"""

import cv2
from PIL import Image
import torch

try:
    from .env import CHECKPOINT_FILE, DEVICE
    from .model import create_model
    from .transforms import test_transform
except ImportError:
    from env import CHECKPOINT_FILE, DEVICE
    from model import create_model
    from transforms import test_transform


def load_face_classifier():
    if not CHECKPOINT_FILE.exists():
        raise FileNotFoundError(
            f"checkpoint가 없습니다: {CHECKPOINT_FILE}"
        )

    checkpoint = torch.load(
        CHECKPOINT_FILE,
        map_location=DEVICE,
    )

    class_to_idx = checkpoint["class_to_idx"]

    idx_to_class = {
        idx: name
        for name, idx in class_to_idx.items()
    }

    model = create_model(
        num_classes=checkpoint["num_classes"],
        freeze_features=True,
    ).to(DEVICE)

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model.eval()

    return model, idx_to_class


@torch.inference_mode()
def predict_face_bgr(
    face_bgr,
    model,
    idx_to_class,
):
    """
    face_bgr:
        OpenCV ndarray, shape=(H, W, 3), BGR

    학습 때와 동일하게:
        BGR -> RGB -> PIL -> test_transform
        -> [1, 3, 224, 224]
    """
    face_rgb = cv2.cvtColor(
        face_bgr,
        cv2.COLOR_BGR2RGB,
    )

    image = Image.fromarray(face_rgb)

    tensor = test_transform(image)
    tensor = tensor.unsqueeze(0).to(DEVICE)

    logits = model(tensor)

    probabilities = torch.softmax(
        logits,
        dim=1,
    )

    confidence, pred_idx = probabilities.max(
        dim=1,
    )

    pred_idx = pred_idx.item()
    confidence = confidence.item()

    class_name = idx_to_class[pred_idx]

    return class_name, confidence
