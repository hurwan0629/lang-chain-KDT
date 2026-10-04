import argparse
from pathlib import Path

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor


MODEL_NAME = "openai/clip-vit-base-patch32"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# LABELS = [
#     "a person writing computer code",
#     "a person studying",
#     "a person writing a document",
#     "a person planning a trip",
#     "a person watching entertainment",
# ]
LABELS = [
    "coding",
    "debugging",
    "studying",
    "reading a paper",
    "taking notes",
    "writing a document",
    "making a presentation",
    "searching the web",
    "reading documentation",
    "planning a trip",
    "using maps",
    "shopping online",
    "writing email",
    "chatting",
    "watching videos",
    "using social media",
    "playing games",
]


def parse_args():
    """분석할 이미지 폴더와 시작 위치, 개수를 명령줄에서 받는다."""
    parser = argparse.ArgumentParser(
        description="여러 스크린샷의 평균 CLIP embedding으로 행동을 추론합니다."
    )
    parser.add_argument(
        "--folder",
        type=Path,
        required=True,
        help="분석할 이미지가 들어 있는 폴더",
    )
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="정렬된 이미지 목록에서 시작할 위치",
    )
    parser.add_argument(
        "--limit",
        type=int,
        required=True,
        help="offset부터 가져올 이미지 개수",
    )
    return parser.parse_args()


def load_clip():
    """사전학습된 CLIP 모델과 전처리기를 불러온다."""
    model = CLIPModel.from_pretrained(MODEL_NAME).to(DEVICE)
    processor = CLIPProcessor.from_pretrained(MODEL_NAME)
    model.eval()

    return model, processor


def load_images(folder: Path, offset: int, limit: int):
    """폴더의 이미지를 정렬한 뒤 offset부터 limit개를 RGB PIL 이미지로 읽는다."""
    if not folder.is_dir():
        raise NotADirectoryError(f"폴더를 찾을 수 없습니다: {folder}")
    if offset < 0:
        raise ValueError("offset은 0 이상이어야 합니다.")
    if limit <= 0:
        raise ValueError("limit은 1 이상이어야 합니다.")

    image_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
    image_paths = sorted(
        path
        for path in folder.iterdir()
        if path.is_file() and path.suffix.lower() in image_extensions
    )

    selected_paths = image_paths[offset : offset + limit]

    if not selected_paths:
        raise ValueError(
            f"선택된 이미지가 없습니다. 전체 이미지 수={len(image_paths)}, offset={offset}"
        )

    images = [Image.open(path).convert("RGB") for path in selected_paths]

    return images, selected_paths


def _get_feature_tensor(features):
    """Transformers 반환 객체에서 실제 feature tensor를 꺼낸다."""
    if isinstance(features, torch.Tensor):
        return features
    if "output_pooler" in features:
        return features["output_pooler"]
    return features["pooler_output"]


def encode_images(model, processor, images):
    """여러 이미지를 정규화한 뒤 평균내어 하나의 CLIP image embedding으로 만든다."""
    inputs = processor(
        images=images,
        return_tensors="pt",
    ).to(DEVICE)

    with torch.inference_mode():
        image_features = model.get_image_features(**inputs)

    image_features = _get_feature_tensor(image_features)

    # 각 이미지 embedding을 먼저 길이 1로 정규화한다.
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)

    # 시간 구간의 이미지 embedding들을 평균낸다.
    mean_feature = image_features.mean(dim=0, keepdim=True)

    # 평균 후 다시 길이 1로 정규화한다.
    mean_feature = mean_feature / mean_feature.norm(dim=-1, keepdim=True)

    return mean_feature


def encode_texts(model, processor, texts):
    """여러 행동 문장을 정규화된 CLIP text embedding으로 변환한다."""
    inputs = processor(
        text=texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
    ).to(DEVICE)

    with torch.inference_mode():
        text_features = model.get_text_features(**inputs)

    text_features = _get_feature_tensor(text_features)

    return text_features / text_features.norm(dim=-1, keepdim=True)


def calculate_similarity(image_features, text_features):
    """
    이미지 embedding과 각 text embedding의 cosine similarity를 계산한다.

    image_features: [1, D]
    text_features:  [N, D]
    return:         [1, N]
    """
    return image_features @ text_features.T


def predict(model, processor, images, labels):
    """여러 이미지의 평균 embedding과 가장 유사한 행동 문장을 반환한다."""
    image_features = encode_images(model, processor, images)
    text_features = encode_texts(model, processor, labels)

    print(f"image_features.shape: {image_features.shape}")
    print(f"text_features.shape: {text_features.shape}")

    similarities = calculate_similarity(
        image_features,
        text_features,
    ).squeeze(0)

    best_index = similarities.argmax().item()

    return labels[best_index], similarities


def main():
    args = parse_args()

    print(f"device: {DEVICE}")
    print(f"folder: {args.folder}")
    print(f"offset: {args.offset}")
    print(f"limit: {args.limit}")

    model, processor = load_clip()
    images, image_paths = load_images(
        args.folder,
        args.offset,
        args.limit,
    )

    print(f"selected images: {len(image_paths)}")
    for image_path in image_paths:
        print(f"  - {image_path}")

    predicted_label, similarities = predict(
        model,
        processor,
        images,
        LABELS,
    )

    # import pandas as pd
    

    print(f"\nprediction: {predicted_label}\n")

    ranked_results = sorted(
        zip(LABELS, similarities.tolist()),
        key=lambda item: item[1],
        reverse=True,
    )

    for label, score in ranked_results:
        print(f"{label:40s}: {str(round(score*100, 2))}")


if __name__ == "__main__":
    main()
