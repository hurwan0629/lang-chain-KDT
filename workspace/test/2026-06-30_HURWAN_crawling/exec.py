import argparse
import sys
from pathlib import Path


PROJECT_DIR = Path(__file__).resolve().parent / "proj"
sys.path.insert(0, str(PROJECT_DIR))

from proj.main import crawl_start


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument("keyword")
  parser.add_argument("yes_pages", type=int)
  parser.add_argument("kyobo_pages", type=int)
  parser.add_argument("aladin_pages", type=int)
  parser.add_argument(
    "path_mode",
    choices=("absolute", "relative"),
  )
  return parser.parse_args()


if __name__ == "__main__":
  args = parse_args()

  crawl_start(
    args.keyword,
    args.yes_pages,
    args.kyobo_pages,
    args.aladin_pages,
    save_path_absolute=args.path_mode == "absolute",
  )
