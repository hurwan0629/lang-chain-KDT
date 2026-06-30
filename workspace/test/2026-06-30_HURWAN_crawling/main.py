from datetime import datetime
from pathlib import Path
# import pprint
import pandas as pd
from my_lib.yes_crawl import yes_crawl
from my_lib.kyobo_crawl import kyobo_crawl
from my_lib.aladin_crawl import aladin_crawl


def crawl_start(keywords, yes_pages, kyobo_pages, aladin_pages):

  # 저장 폴더들 정리

  folder_name = f"search_{datetime.now().year}-{datetime.now().month:02d}-{datetime.now().day:02d}_{datetime.now().hour:02d}H{datetime.now().minute:002d}m{datetime.now().second:02d}s_[{keywords}]_[{yes_pages}]_[{kyobo_pages}]_[{aladin_pages}]"
  SAVE_DIR = Path(__file__) / ".." / "datas" / folder_name

  print(SAVE_DIR)

  if not SAVE_DIR.exists():
    SAVE_DIR.mkdir(parents=True, exist_ok=True)

  IMG_DIR = SAVE_DIR / "images"

  IMG_DIR.mkdir(exist_ok=True)

  # # # # # # # # # # # # # # # 크롤링 작업 # # # # # # # # # # # # # # # 
  # 크롤링 시작하기
  yes_dict_list = None
  aladin_dict_list = None
  kyobo_dict_list = None

  # 예스24 크롤링
  try:
    yes_dict_list = yes_crawl(keywords, yes_pages, (IMG_DIR / "yes24"))
  except Exception as e:
    print(e)
    print("예스24 크롤링 중 예상하지 못한 예외 발생")
    print("다음 작업을 재게합니다.")
  
  # 교보 크롤링
  try:
    kyobo_dict_list = kyobo_crawl(keywords, kyobo_pages, (IMG_DIR / "kyobo"))
  except Exception as e:
    print(e)
    print("교보 크롤링 중 예상하지 못한 예외 발생")
    print("다음 작업을 재게합니다.")
  
  # 알라딘 크롤링
  try:
    aladin_dict_list = aladin_crawl(keywords, aladin_pages, (IMG_DIR / "aladin"))
  except Exception as e:
    print(e)
    print("알라딘 크롤링 중 예상하지 못한 예외 발생")
    print("다음 작업을 재게합니다.")
  
  # # # # # # # # # # # # # # # 데이터 처리 작업 # # # # # # # # # # # # # # # 
  with pd.ExcelWriter((SAVE_DIR / "datas.xlsx")) as writer:
    #
    # 각각 수행할 작업
    # 0. None(데이터 없음) 이 아니라면
    # 1. DF로 만들기
    # 2. 키워드 앞에 달아주기 (왜 달아야하는지 싶지만 요구사항이니 수행)
    # 3. writer을 통해 시트에 작성

    # 예스24
    if yes_dict_list is not None:
      yes_df = pd.DataFrame(yes_dict_list, columns=list(yes_dict_list[0].keys()))
      yes_df.insert(0, "keyword", keywords)
      yes_df.to_excel(writer, sheet_name="yes24", index=False)

    # 교보
    if kyobo_dict_list is not None:
      kyobo_df = pd.DataFrame(kyobo_dict_list, columns=list(kyobo_dict_list[0].keys()))
      kyobo_df.insert(0, "keyword", keywords)
      kyobo_df.to_excel(writer, sheet_name="kyobo", index=False)

    # 알라딘
    if aladin_dict_list is not None:
      aladin_df = pd.DataFrame(aladin_dict_list, columns=list(aladin_dict_list[0].keys()))
      aladin_df.insert(0, "keyword", keywords)
      aladin_df.to_excel(writer, sheet_name="aladin", index=False)



if __name__ == "__main__":
  crawl_start('머ㅁㄴㅇㄹ모ㅓㅏㅁㄴ허ㅚㄴㅂㅁ해;ㅗㄴㅇㅁ호;ㅕㅓ니', 1, 1, 1)