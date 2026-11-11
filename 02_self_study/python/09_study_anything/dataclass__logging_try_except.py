from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import logging
import yaml

@dataclass
class TrainConfig:
  model: str = "yolo11n"
  epochs: int = 100
  batch_size: int = 16
  output: str = "outputs"

logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

def parse_args():
  parser = argparse.ArgumentParser(
    description="YOLO 학습 설정 관리"
  )

  parser.add_argument("--model", default="yolo11n")
  parser.add_argument("--epochs", type=int, default=100)
  parser.add_argument("--batch-size", type=int, default=16)
  parser.add_argument("--output", default="outputs")

  return parser.parse_args()

def save_config(config: TrainConfig):
  output_dir = Path(config.output)
  output_dir.mkdir(parents=True, exist_ok=True)

  path = output_dir / "config.yaml"

  with path.open("w", encoding="utf-8") as f:
    yaml.safe_dump(
      asdict(config), f,
      allow_unicode=True,
      sort_keys=False
    )

  logger.info("설정 저장: %s", path)
  return path

def load_config(path: Path) -> TrainConfig:
  with path.open("r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

  return TrainConfig(**data)

def main():
  args = parse_args()

  config = TrainConfig(
    model=args.model,
    epochs=args.epochs,
    batch_size=args.batch_size,
    output=args.output
  )

  try:
    if config.epochs <= 0:
      raise ValueError("epochs는 1 이상이어야 합니다.")

    path = save_config(config)
    loaded = load_config(path)
    logger.info("설정: %s", loaded)

  except(OSError, ValueError, yaml.YAMLError) as e:
    logger.error("실행 실패: %s", e)
    raise SystemExit(1) from e


if __name__ == "__main__":
  main()
