from pathlib import Path
import json

# 1. 현재 파일을 기준으로 작업 폴더 지정
# Path.cwd는 프로그램이 실행되는 현재 디렉토리를 의미함.
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "datasets"
OUTPUT_DIR = BASE_DIR / "outputs"

# 2. 폴더 생성
# 현재 폴더를 기준으로 작성. 
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 3. 설정 데이터
config = {
  "model": "yolo11n",
  "epochs": 100,
  "classes": ["bottle", "can", "paper"]
}

# 4. JSON 파일로 저장
config_path = DATA_DIR / "config.json"

# 설정 파일에 만들어둔 json 파일 작성하기 -> 줄내림 + 2칸 들여쓰기
config_path.write_text(
  # dumps -> str -> path에 작성해주기
  json.dumps(config, indent=2, ensure_ascii=False),
  encoding="utf-8"
)

# 5. JSON 파일 읽기
loaded = json.loads(
  config_path.read_text(encoding="utf-8")
)

print(loaded)