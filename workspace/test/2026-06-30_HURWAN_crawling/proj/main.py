from datetime import datetime
from pathlib import Path
import time
# import pprint
import pandas as pd
from my_lib.yes_crawl import yes_crawl
from my_lib.kyobo_crawl import kyobo_crawl
from my_lib.aladin_crawl import aladin_crawl


def crawl_start(keywords: str, yes_pages: int, kyobo_pages: int, aladin_pages: int, save_path_absolute: bool=True):
  print("\n[전체 시작] 도서 크롤링\n")
  start = datetime.now()

  # # # # # # # # # # # # # # # 값 체크 # # # # # # # # # # # # # # # 
  # 키워드를 문자열로 바꿔주기
  keywords = str(keywords)

  # 페이지들 문자열이거나 숫자가 이상하면 돌려보내기
  try:
    int(yes_pages)
    int(kyobo_pages)
    int(aladin_pages)
    if yes_pages < 0 or kyobo_pages < 0 or aladin_pages < 0:
      raise Exception
  except:
    print("[오류] 페이지 수는 0 이상의 정수여야 합니다.")
    return
  
  if not isinstance(save_path_absolute, bool):
    print("[오류] save_path_absolute 인자에는 bool 타입만 들어갈 수 있습니다.")
    return
  # # # # # # # # # # # # # # # 최초 자원 설정 # # # # # # # # # # # # # # # 
  # 저장 폴더들 정리

  folder_name = f"search_{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}_{datetime.now().hour:02d}H{datetime.now().minute:002d}m{datetime.now().second:02d}s_[{keywords}]_[{yes_pages}]_[{kyobo_pages}]_[{aladin_pages}]"
  
  
  SAVE_DIR = Path(__file__) / ".." / ".." / "datas" / folder_name

  print(f"[저장 위치] {SAVE_DIR}")

  if not SAVE_DIR.exists():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

  IMG_DIR = SAVE_DIR / "images"

  IMG_DIR.mkdir(exist_ok=True)

  def to_relative_image_path(image_link):
    if pd.isna(image_link) or image_link in ("", "None"):
      return image_link

    try:
      return Path(image_link).resolve().relative_to(
        SAVE_DIR.resolve()
      ).as_posix()
    except (ValueError, OSError):
      # 외부 URL이거나 SAVE_DIR 외부 경로라면 기존 값 유지
      return image_link

  # # # # # # # # # # # # # # # 크롤링 작업 # # # # # # # # # # # # # # # 
  # 크롤링 시작하기
  yes_dict_list = None
  aladin_dict_list = None
  kyobo_dict_list = None

  # 예스24 크롤링
  try:
    if yes_pages < 0:
      raise ValueError
    yes_dict_list = yes_crawl(keywords, yes_pages, (IMG_DIR / "yes24"))
  except Exception as e:
    print(e)
    print("[오류] YES24 크롤링 실패")
    print("[계속] 다음 사이트 작업을 재개합니다.")
  
  # 교보 크롤링
  try:
    kyobo_dict_list = kyobo_crawl(keywords, kyobo_pages, (IMG_DIR / "kyobo"))
  except Exception as e:
    print(e)
    print("[오류] 교보 크롤링 실패")
    print("[계속] 다음 사이트 작업을 재개합니다.")
  
  # 알라딘 크롤링
  try:
    aladin_dict_list = aladin_crawl(keywords, aladin_pages, (IMG_DIR / "aladin"))
  except Exception as e:
    print(e)
    print("[오류] 알라딘 크롤링 실패")
    print("[계속] 다음 사이트 작업을 재개합니다.")
  
  # # # # # # # # # # # # # # # 데이터 처리 작업 # # # # # # # # # # # # # # # 
  with pd.ExcelWriter((SAVE_DIR / "datas.xlsx")) as writer:
    #
    # 각각 수행할 작업
    # 0. None(데이터 없음) 이 아니라면
    # 1. DF로 만들기
    # - save_path_absolute==True이면 SAVE_DIR 기준으로 위치 잡아주기
    # 2. 키워드 앞에 달아주기 (왜 달아야하는지 싶지만 요구사항이니 수행)
    # 3. writer을 통해 시트에 작성

    # 예스24
    if yes_dict_list is not None:
      yes_df = pd.DataFrame(yes_dict_list, columns=list(yes_dict_list[0].keys()))
      
      # 상대경로 지정을 원한다면 상대경로로 바꿔주기
      if not save_path_absolute:
        yes_df["image_link"] = yes_df["image_link"].map(to_relative_image_path)
      
      # 마저 작업 해주기
      yes_df.insert(0, "keyword", keywords)
      yes_df.to_excel(writer, sheet_name="yes24", index=False)

    # 교보
    if kyobo_dict_list is not None:
      kyobo_df = pd.DataFrame(kyobo_dict_list, columns=list(kyobo_dict_list[0].keys()))

      # 상대경로 지정을 원한다면 상대경로로 바꿔주기
      if not save_path_absolute:
        kyobo_df["image_link"] = kyobo_df["image_link"].map(to_relative_image_path)
      
      # 마저 작업 해주기
      kyobo_df.insert(0, "keyword", keywords)
      kyobo_df.to_excel(writer, sheet_name="kyobo", index=False)

    # 알라딘
    if aladin_dict_list is not None:
      aladin_df = pd.DataFrame(aladin_dict_list, columns=list(aladin_dict_list[0].keys()))

      # 상대경로 지정을 원한다면 상대경로로 바꿔주기
      if not save_path_absolute:
        aladin_df["image_link"] = aladin_df["image_link"].map(to_relative_image_path)

      # 마저 작업 해주기
      aladin_df.insert(0, "keyword", keywords)
      aladin_df.to_excel(writer, sheet_name="aladin", index=False)

    end = datetime.now()

    print("[전체 종료] 도서 크롤링")
    print(f"[소요 시간] {end - start}")
    print(f"[저장 위치] {SAVE_DIR}")


if __name__ == "__main__":
  # crawl_start('sqld', 1, 2, 4)
  crawl_start('이방인', 1, 8, 20, save_path_absolute=False)
