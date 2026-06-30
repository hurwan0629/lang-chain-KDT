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

from .config import YES_URL, EXT_MAP


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
def yes_crawl(keywords: str, pages: int, YES_IMG_DIR) -> Optional[list | None]:
  print(" =============================== ")
  print(" ======= 예스24 크롤링 시작 ====== ")
  print(" =============================== ")

  # # # # # # # # # # # # # # # # # # # # 설정 # # # # # # # # # # # # # # # # # # # # 

  options = Options()
  options.add_argument("--start-maximized")

  driver = webdriver.Chrome(options)

  wait = WebDriverWait(driver, 10)

  # # # # # # # # # # # # # # # # # # # # 설정 # # # # # # # # # # # # # # # # # # # # 

  # # # # # # # # # # # # # # # # # # # 작업 시작 [페이지 순회 전 작업] # # # # # # # # # # # # # # # # # # # 

  print("     검색 설정중...    ")

  # url 들어가기
  driver.get(YES_URL)

  # input 입력창 선택하기
  search_bar = wait.until(
    EC.element_to_be_clickable(
      (By.CSS_SELECTOR, "input#query")
    )
  )

  # 키워드 입력 후 enter 누르기
  search_bar.clear()
  search_bar.send_keys(keywords)
  search_bar.send_keys(Keys.ENTER)

  
  # 결과 있는지 확인하기
  time.sleep(3)
  search_success = True
  try:
    driver.find_element(By.CSS_SELECTOR, "div.noData.schData")
    search_success=False
  except NoSuchElementException as e:
    pass
  if not search_success:
    print("예스24 검색결과 없음")
    # input("예스24 스톱")
    return None


  # 도서 정보만 뽑기 위해 "국내도서" 버튼 찾아서 눌러주기
  wait.until(
    EC.element_to_be_clickable(
      (By.XPATH, "//a[.//span[contains(text(), '국내도서')]]")
    )
  ).click()

  # 도서명,저자/역자,출판사 조건 걸고 AI 활용 끄기
  try:
    wait.until(
      EC.element_to_be_clickable(
        (By.XPATH, "//label[.//input[@value='TITLE'] and contains(., '도서명')]")
      )
    ).click()
  except Exception as e:
    # 치명적인 에러가 아니기 때문에 계속 진행
    pass

  time.sleep(3)

  try:
    wait.until(
      EC.element_to_be_clickable(
        (By.XPATH, "//label[.//input[@value='AUTHOR'] and contains(., '저자/역자')]")
      )
    ).click()
  except Exception as e:
    # 치명적인 에러가 아니기 때문에 계속 진행
    pass
  time.sleep(3)

  try:
    wait.until(
      EC.element_to_be_clickable(
        (By.XPATH, "//label[.//input[@value='COMPANY'] and contains(., '출판사')]")
      )
    ).click()
  except Exception as e:
    # 치명적인 에러가 아니기 때문에 계속 진행
    pass

  time.sleep(3)

  try:
    wait.until(
      EC.element_to_be_clickable(
        (By.XPATH, "//label[.//input[@name='includeAI' and @data-search-type='aiUseYn'] and contains(., 'AI 활용 콘텐츠 제외')]")
      )
    ).click()
  except Exception as e:
    # 치명적인 에러가 아니기 때문에 계속 진행
    pass


  # # # # # # # # # # # # # # # # # # # 페이지 순회 시작 # # # # # # # # # # # # # # # # # # # 
  # 페이지개수만큼 돌아주기.
  # 도는 조건은 (다음 `(>)` 버튼이 존재하면 계속 가주기)
  book_datas = []
  book_num = 1
  for i in range(pages):
    # 스크롤 맨 아래까지 내리기
    target_element = driver.find_element(By.CSS_SELECTOR, "div.yesUI_pagen")
    driver.execute_script("arguments[0].scrollIntoView();", target_element)

    time.sleep(2)
    # 현재 크롤링 페이지 출력
    print(f"\n --- 예스24 {i+1}페이지 --- \n")
    # 페이지 전체 긁어주기 도서 정보들
    book_lists = wait.until(
      EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "ul#yesSchList > li")
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
        title = book.find_element(By.CSS_SELECTOR, "div.info_row.info_name > a.gd_name").text.strip()
      except NoSuchElementException as e:
        pass
        # print("제목 없음")
      # print(title)
      
      # 저자
      author = ""
      try:
        author = book.find_element(By.CSS_SELECTOR, "div.info_pubGrp > span.info_auth").text.strip()
      except NoSuchElementException as e:
        # print("제목 없음")
        pass
      # print(author)
      
      # 가격
      price = ""
      try:
        price = book.find_element(By.CSS_SELECTOR, ".info_price strong.txt_num .yes_b").text.strip().replace(",", "").replace(" ", "")
      except NoSuchElementException as e:
        # print("가격 없음")
        pass
      # print(price)
      
      # 출판사
      
      publisher = ""
      try:
        publisher = book.find_element(By.CSS_SELECTOR, ".info_pubGrp .info_pub a").text.strip()
      except NoSuchElementException as e:
        # print("작가 없음 없음")
        pass
      # print(publisher)
      
      # 출판일
      pub_date = ""
      try:
        pub_date = book.find_element(By.CSS_SELECTOR, ".info_pubGrp .info_date").text.strip()
      except NoSuchElementException as e:
        # print("출판일 없음")
        pass
      # print(pub_date)
      
      # 이미지 상대 경로
      image_link = ""
      try:
        img = book.find_element(By.CSS_SELECTOR, ".item_img img")
        image_link = img.get_attribute("data-original") or img.get_attribute("src")
        # print(image_link)
        # 이미지 저장

        YES_IMG_DIR.mkdir(exist_ok=True)

        if image_link is not None:
          res = requests.request("GET", image_link)
          ext = res.headers.get("Content-Type", None)
          # print(f"응답 확장자: {ext}")

          # 응답이 잘 오면 이미지 저장해주기
          if res.ok and ext is not None:
            ext = EXT_MAP.get(ext, ".jpg")
            image_link = YES_IMG_DIR / (str(uuid.uuid4()) + ext)
            # image_link = YES_IMG_DIR / (str(book_num) + ext)
            book_num+=1
            with open(image_link, "wb") as f:
              f.write(res.content)
            print(f"[이미지 저장] [{title}] 저장 완료!")
          else:
            print(f"[이미지 저장] [{title}] 이미지 없음!")
      except NoSuchElementException as e:
        print("이미지 없음")
      
      # 데이터 book_datas 에 append 해주기
      book_datas.append({
        "title": title,
        "author": author,
        "price": price,
        "publisher": publisher,
        "pub_date": pub_date,
        "image_link": str(image_link),
      })
      print(f"{len(book_datas)}번째 데이터 추가 완료: {title}\n")
  
    # 
      
    # # # # # # # # # # # # # # # # # # # 한페이지 순회 종료 # # # # # # # # # # # # # # # # # # # 
    # 다음 페이지 있으면 다음 페이지 가주기
    # 페이지네이션 박스 찾기
    # 페이지들 뽑기
    pages_ui = wait.until(
      EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, ".yesUI_pagen > *")
      )
    )
    
    pgn_status = ""
    go_next = False
    pgn_btn_to_click = None
    for p in pages_ui:
      if p.tag_name == "strong":
        pgn_status += p.text + "[현위치]  "
        go_next = True
      elif p.tag_name == "a" and go_next == True:
        pgn_status += p.text + "[누를 예정]  "
        pgn_btn_to_click = p
        go_next = False
      elif p.tag_name == "a":
        pgn_status += p.text + "[활성화]  "
    
    print()
    print(f"현재 상태: {pgn_status}")
    if pgn_btn_to_click is not None:
      print(pgn_btn_to_click.text + " 클릭")
      time.sleep(1)
      pgn_btn_to_click.click()
    else:
      print("\n --- 예스 24 크롤링 종료 --- \n")
      return book_datas
    
  print("\n --- 예스 24 크롤링 종료 --- \n")
  return book_datas