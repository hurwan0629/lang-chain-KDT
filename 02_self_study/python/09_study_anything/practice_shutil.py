from pathlib import Path
import shutil

source = Path("here/config.yaml")
backup = Path("practice_output/config.yaml")

backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(source, backup)

print("원본 존재:", source.exists())
print("백업 존재:", backup.exists())
print("내용 동일:", source.read_bytes() == backup.read_bytes())
