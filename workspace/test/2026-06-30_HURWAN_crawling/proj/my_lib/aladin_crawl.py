# import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains

import time
import re
import pandas as pd
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import requests
import uuid
from typing import Optional

from .config import ALADIN_URL, EXT_MAP


# # # # # # # # # # # # # # # # # # # # 초기화 # # # # # # # # # # # # # # # # # # # # 

# 상수
# YES_URL = "http://www.yes24.com/Main/default.aspx"
# EXT_MAP = {
#     "image/jpeg": ".jpg",
#     "image/png": ".png",
#     "image/webp": ".webp",
#     "image/gif": ".gif",
# }
# # 
# keywords = "안녕하세요"
# pages = 20
def aladin_crawl(keywords: str, pages: int, ALADIN_IMG_DIR) -> Optional[list | None]:
  print("================================")
  print("[시작] 알라딘 크롤링")
  print("================================")

  # # # # # # # # # # # # # # # # # # # # 설정 # # # # # # # # # # # # # # # # # # # # 

  options = Options()
  options.add_argument("--start-maximized")

  driver = webdriver.Chrome(options)

  wait = WebDriverWait(driver, 10)

  # # # # # # # # # # # # # # # # # # # # 설정 # # # # # # # # # # # # # # # # # # # # 

  # # # # # # # # # # # # # # # # # # # 작업 시작 [페이지 순회 전 작업] # # # # # # # # # # # # # # # # # # # 

  print("[준비] 알라딘 검색 설정 중...")

  # url 들어가기
  driver.get(ALADIN_URL)

  print("[준비] 알라딘 검색 중...")
  # input 입력창 선택하기
  search_bar = wait.until(
    EC.element_to_be_clickable(
      (By.CSS_SELECTOR, "input#SearchWord")
    )
  )

  # 키워드 입력 후 enter 누르기
  search_bar.clear()
  for k in keywords:
    search_bar.send_keys(k)
  search_bar.send_keys(Keys.ENTER)
  

  time.sleep(3)
  # 교보 브레이크
  # input("교보 브레이커")
  # 결과 있는지 확인하기
  search_success = True
  try:
    if f"'{keywords}'에 대한 검색 결과가 없습니다." == str(driver.find_element(By.CSS_SELECTOR, "div.ss_line div.search_t_g").text).strip():
      search_success=False
    
  except NoSuchElementException as e:
    pass
  if not search_success:
    print("[경고] 알라딘 검색 결과 없음")
    # input("교보 브레이커")
    return None
  
  print("[알람] 알라딘 탐색 시작")
  # # # # # # # # # # # # # # # # # # # 페이지 순회 시작 # # # # # # # # # # # # # # # # # # # 
  # 페이지개수만큼 돌아주기.
  # 도는 조건은 (다음 `(>)` 버튼이 존재하면 계속 가주기)
  book_datas = []
  book_num = 1
  for i in range(pages):
    # 스크롤 맨 아래까지 내리기
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    time.sleep(2)
    # 현재 크롤링 페이지 출력
    print(f"\n[페이지] 알라딘 | {i+1}페이지\n")
    # 페이지 전체 긁어주기 도서 정보들
    book_lists = wait.until(
      EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div#Search3_Result > div")
      )
    )

    # print(book_lists[-1].get_attribute("innerHTML"))
    # 도서들 순회하기
    for book in book_lists:
      # print(book.get_attribute("innerHTML"))
      # 책제목	저자	가격	출판사	출판일	이미지(저장 후 상대경로)
      
      # print(book.get_attribute("innerHTML"))

      # 제목
      title = ""
      try:
        title = book.find_element(By.CSS_SELECTOR, ".ss_book_list a.bo3").text.strip()
      except NoSuchElementException as e:
        # print("제목 정보 없음")
        pass
      # print(title)
      
      
      # 가격
      price = ""
      try:
        price = book.find_element(By.CSS_SELECTOR, ".ss_book_list span.ss_p2 em").text.strip().replace(",", "").replace(" ", "").replace("원", "")
      except NoSuchElementException as e:
        # print("가격 정보 없음")
        pass
      # print(price)
      
      # 저자 출판사 출판일
      # li 1번에 span.ss_ht1 가 있으면 3번쨰로, 없으면 2번째로
            # 저자·출판사·출판일 후보를 2번째, 3번째 li에서 모두 확인
      pattern = r"^\s*(?P<author>.*?)\s*\|\s*(?P<publisher>.*?)\s*\|\s*(?P<pub_date>\d{4}년\s*\d{1,2}월)\s*$"
      auth_candidates = []
      for selector in (
        ".ss_book_list > ul > li:nth-child(2)",
        ".ss_book_list > ul > li:nth-child(3)",
      ):
        elements = book.find_elements(By.CSS_SELECTOR, selector)
        if elements:
          auth_candidates.append(elements[0].text.strip())
      # 정규식에 맞는 첫 번째 후보 선택
      auth_str = next(
        (
          candidate
          for candidate in auth_candidates
          if re.fullmatch(pattern, candidate)
        ),
        "",
      )
      match = re.fullmatch(pattern, auth_str)
      author = ""
      publisher = ""
      pub_date = ""
      if match:
        author = match.group("author")
        publisher = match.group("publisher")
        pub_date = match.group("pub_date")
      else:
        # print("저자·출판사·출판일 정보 없음")
        pass


      # 이미지 뽑기 테스트
      # try:
      #   img = book.find_element(By.CSS_SELECTOR, ".cover_area img.front_cover")
      #   image_link = img.get_attribute("data-original") or img.get_attribute("src")
      #   print(image_link)
      # except Exception as e:
      #   try:
      #     img = book.find_element(By.CSS_SELECTOR, ".cover_area_other > a > img:first-of-type")
      #     image_link = img.get_attribute("data-original") or img.get_attribute("src")
      #     print(image_link)
      #   except Exception as e:
      #     print("이미지 없음")
  
      # 이미지 상대 경로
      image_link = None
      try:
        try:
          img = book.find_element(By.CSS_SELECTOR, ".cover_area img.front_cover")
          image_link = img.get_attribute("data-original") or img.get_attribute("src")
          # print(image_link)
        except Exception as e:
          try:
            img = book.find_element(By.CSS_SELECTOR, ".cover_area_other > a > img:first-of-type")
            image_link = img.get_attribute("data-original") or img.get_attribute("src")
            # print(image_link)
          except Exception as e:
            print("[이미지] 없음")
        # print(image_link)
        # 이미지 저장

        ALADIN_IMG_DIR.mkdir(exist_ok=True)

        if image_link is not None:
          res = requests.request("GET", image_link)
          ext = res.headers.get("Content-Type", None)
          # print(f"응답 확장자: {ext}")

          # 응답이 잘 오면 이미지 저장해주기
          if res.ok and ext is not None:
            ext = EXT_MAP.get(ext, ".jpg")
            image_link = ALADIN_IMG_DIR / (str(uuid.uuid4()) + ext)
            # image_link = YES_IMG_DIR / (str(book_num) + ext)
            book_num+=1
            with open(image_link, "wb") as f:
              f.write(res.content)
            print(f"[이미지] 저장 완료 | {title}")
          else:
            print(f"[이미지] 없음 | {title}")
      except NoSuchElementException as e:
        print("[이미지] 없음")
      
      # 데이터 book_datas 에 append 해주기
      book_datas.append({
        "title": title,
        "author": author,
        "price": price,
        "publisher": publisher,
        "pub_date": pub_date,
        "image_link": str(image_link),
      })
      print(f"[완료] {len(book_datas)}번째 도서 | {title}\n")
    
    # # # # # # # # # # # # # # # # # # # 한페이지 순회 종료 # # # # # # # # # # # # # # # # # # # 
    # 다음 페이지 있으면 다음 페이지 가주기
    # 페이지네이션 박스 찾기
    # 페이지들 뽑기
    pages_ui = wait.until(
      EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div.Search3_Pager")
      )
    )[0].find_elements(By.CSS_SELECTOR, "div#short a")
    
    go_next = False
    pgn_btn_to_click = None
    for p in pages_ui:
      if go_next and "numoff" in str(p.get_attribute("class")).split(" "):
        print(f"[{p.text}]  ", end="")
        go_next = False
        pgn_btn_to_click = p
      elif "numon" in str(p.get_attribute("class")).split(" "):
        print(f"<{p.text}>  ", end="")
        go_next = True
      else:
        print(f"[{p.text}]  ", end="")
    
    # input("알라딘 브레이커")
    if pgn_btn_to_click is None:
      print("\n[종료] 알라딘 크롤링 | 마지막 페이지 도달\n")
      return book_datas
    else:
      pgn_btn_to_click.click()
  print("\n[종료] 알라딘 크롤링\n")
  return book_datas
    
