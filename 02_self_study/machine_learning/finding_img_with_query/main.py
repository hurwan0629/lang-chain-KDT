import torch

from PIL import Image
from transformers import AutoProcessor, CLIPModel

MODEL_NAME = "openai/clip-vit-base-patch32"

breakpoint()
# 실제 신경망 역할
# from_pretrained는 이미 학습된 모델/전처리 설정을 가져오는 메서드
model = CLIPModel.from_pretrained(MODEL_NAME)
# 이미지/텍스트를 CLIP에 넣을 수 있는 형태로 전처리
# 이미 학습된 Image Encoder, Text Encoder 을 사용함
# PIL 이미지 -> resize -> normalize -> Tensor
# 문자열 -> tokenize -> input_ids -> Tensor
processor = AutoProcessor.from_pretrained(MODEL_NAME)

# 각각의 이미지 및 문장을 CLIP에 넣어주게 되면 image/text embedding 이 되게 됩니다.

print(type(model))
print(type(processor))

breakpoint()

image = Image.open("images/cchamppang.png")

inputs = processor(
  images=image,
  return_tensors="pt"
)

print(inputs)

image = image.convert("RGB")

inputs = processor(
  images=image,
  return_tensors="pt"
)
print(inputs["pixel_values"].shape)