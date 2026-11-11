from pathlib import Path
import argparse
import yaml

# CLI 인자 정의
parser = argparse.ArgumentParser(
  description="YOLO 학습 설정 관리"
)

parser.add_argument(
  "--model",
  type=str,
  default="yolo11n",
  help="사용할 모델 이름"
)

parser.add_argument(
  "--epochs",
  type=int,
  default=100,
  help="학습 반복 횟수"
)

parser.add_argument(
  "--output",
  type=Path,
  default=Path("outputs"),
  help="결과 저장 폴더"
)

args = parser.parse_args()

# 설정 데이터 구성
config = {
  "model": args.model,
  "epochs": args.epochs,
  "output": str(args.output),
  "classes": ["bottle", "can", "paper"]
}

# 폴더 및 YAML 파일 생성
args.output.mkdir(parents=True, exist_ok=True)
config_path = args.output / "config.yaml"

with config_path.open("w", encoding="utf-8") as f:
  yaml.safe_dump(
    config,
    f,
    allow_unicode=True,
    sort_keys=False
  )

# yaml 다시 읽기
with config_path.open("r", encoding="utf-8") as f:
  loaded = yaml.safe_load(f)

print("모델:", loaded["model"])
print("Epochs:", loaded["epochs"])
print("클래스;", loaded["classes"])
print("저장 위치:", config_path.resolve)
print(f"""
laoded yaml:
{loaded}
""")