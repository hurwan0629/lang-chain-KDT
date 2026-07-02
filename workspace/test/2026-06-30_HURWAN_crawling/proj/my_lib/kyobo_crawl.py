# import requests
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
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

from .config import KYOBO_URL, EXT_MAP



def kyobo_crawl(keywords: str, pages: int, KYOBO_IMG_DIR) -> Optional[list | None]:
  print("================================")
  print("[시작] 교보 크롤링")
  print("================================")

  # # # # # # # # # # # # # # # # # # # # 설정 # # # # # # # # # # # # # # # # # # # # 

  options = Options()
  options.add_argument("--start-maximized")

  driver = webdriver.Chrome(options)

  wait = WebDriverWait(driver, 10)

  actions = ActionChains(driver=driver)

  # # # # # # # # # # # # # # # # # # # # 설정 # # # # # # # # # # # # # # # # # # # # 

  # # # # # # # # # # # # # # # # # # # 작업 시작 [페이지 순회 전 작업] # # # # # # # # # # # # # # # # # # # 

  print("[준비] 교보 검색 설정 중...")

  # url 들어가기
  driver.get(KYOBO_URL)
  print("[준비] 교보 검색 중...")
  # input 입력창 선택하기
  search_bar = wait.until(
    EC.element_to_be_clickable(
      (By.CSS_SELECTOR, "input#searchKeyword")
    )
  )

  # 키워드 입력 후 enter 누르기
  # driver.execute_script(f"arguments[0].value = '{keywords}'", search_bar)
  time.sleep(0.2)

  # search_bar.send_keys(keywords)
  search_bar.click()
  search_bar.clear()
  for k in keywords:
    search_bar.send_keys(k)
    time.sleep(0.1)
  search_bar.send_keys(Keys.ENTER)


  # 교보 브레이크
  # input("교보 브레이커")
  # 결과 있는지 확인하기
  time.sleep(3)
  search_success = True
  try:
    driver.find_element(By.CSS_SELECTOR, "div.no_data_desc")
    search_success=False
  except NoSuchElementException as e:
    pass
  if not search_success:
    print("[경고] 교보 검색 결과 없음")
    # input("교보 브레이커")
    return None

  print("[알람] 교보 탐색 시작")
  # # # # # # # # # # # # # # # # # # # 페이지 순회 시작 # # # # # # # # # # # # # # # # # # # 
  # 페이지개수만큼 돌아주기.
  # 도는 조건은 (다음 `(>)` 버튼이 존재하면 계속 가주기)
  book_datas = []
  book_num = 1
  for i in range(pages):
    # 스크롤 맨 아래까지 내리기
    target_element = wait.until(
      EC.presence_of_element_located(
        (By.ID, "pagi")
      )
    )
    driver.execute_script("arguments[0].scrollIntoView();", target_element)

    time.sleep(2)
    # 현재 크롤링 페이지 출력
    print(f"\n[페이지] 교보 | {i+1}페이지\n")
    # 페이지 전체 긁어주기 도서 정보들
    book_lists = wait.until(
      EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "div#shopData_list > ul.prod_list > li")
      )
    )

    # with open(Path() / "example.html", "w", encoding="utf-8") as f:
    #   f.write(str(book_lists[-1].get_attribute("innerHTML")))
    # print(len(book_lists))

    # print(book_lists[-1].get_attribute("innerHTML"))
    # 도서들 순회하기
    for book in book_lists:
      # print(book.get_attribute("innerHTML"))
      # 책제목	저자	가격	출판사	출판일	이미지(저장 후 상대경로)
      
      # print(book.get_attribute("innerHTML"))

      # 제목
      title = ""
      try:
        title = book.find_element(By.CSS_SELECTOR, ".prod_name_group a.prod_info span[id^='cmdtName_']").text.strip()
      except NoSuchElementException as e:
        # print("제목 정보 없음")
        pass
      # print(title)
      
      # 저자
      author = ""
      try:
        author = book.find_element(By.CSS_SELECTOR, ".prod_author_info a.author").text.strip()
      except NoSuchElementException as e:
        pass
        # print("저자 정보 없음")
      # print(author)
      
      # 가격
      price = ""
      try:
        price = book.find_element(By.CSS_SELECTOR, ".prod_price .price .val").text.strip().replace(",", "")
      except NoSuchElementException as e:
        try:
          price = book.find_element(By.CSS_SELECTOR, ".prod_coupon_info .price .val").text.strip().replace(",", "")
        except NoSuchElementException as e:
          # print(book.get_attribute("innerHTML"))
          # print("가격 정보 없음")
          pass
      # print(price)
      
      # 출판사
      
      publisher = ""
      try:
        publisher = book.find_element(By.CSS_SELECTOR, ".prod_publish a.text").text.strip()
      except NoSuchElementException as e:
        # print("출판사 정보 없음")
        pass
      # print(publisher)
      
      # 출판일
      pub_date = ""
      try:
        pub_date = book.find_element(By.CSS_SELECTOR, ".prod_publish .date").text.strip()
      except NoSuchElementException as e:
        # print("출판일 정보 없음")
        pass
      # print(pub_date)
      
      

      # 이미지 상대 경로
      image_link = ""
      try:
        img = book.find_element(By.CSS_SELECTOR, ".prod_thumb_box img")
        image_link = img.get_attribute("data-original") or img.get_attribute("src")
        # print(image_link)
        # print(image_link)
        # 이미지 저장

        KYOBO_IMG_DIR.mkdir(exist_ok=True)

        if image_link is not None:
          res = requests.request("GET", image_link)
          ext = res.headers.get("Content-Type", None)
          # print(f"응답 확장자: {ext}")

          # 응답이 잘 오면 이미지 저장해주기
          if res.ok and ext is not None:    
            ext = EXT_MAP.get(ext, ".jpg")
            image_link = KYOBO_IMG_DIR / (str(uuid.uuid4()) + ext)
            # image_link = KYOBO_IMG_DIR / (str(book_num) + ext)
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
    
    # 
      
    # # # # # # # # # # # # # # # # # # # 한페이지 순회 종료 # # # # # # # # # # # # # # # # # # # 
      # 다음 페이지 있으면 다음 페이지 가주기
      # 페이지네이션 박스 찾기
      # 페이지들 뽑기

      # 교보 페이지네이션 구조
      # button.btn_page.prev
      # div.page_num > a
      # button.btn_page.next
      # time.sleep(3)
      # driver.get("https://search.kyobobook.co.kr/search?keyword=%EA%B2%8C%EC%9E%84&target=total&gbCode=TOT&page=6578")
      # time.sleep(3)

    pages_nums = wait.until(
      EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "#pagi > div.page_num > a")
      )
    )
    
    pages_next = wait.until(
      EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "#pagi > button.btn_page.next")
      )
    )
    print()

    print("[페이지 이동] 교보 | [이전]  ", end="")
    for p in pages_nums:
      if 'active' in str(p.get_attribute("class")).split(" "):
        print(f"<{p.text}>  ", end="")
      else:
        print(f"[{p.text}]  ", end="")
    print("[다음]")

    if pages_next.get_attribute("disabled") == "true":
      print("\n[종료] 교보 크롤링 | 마지막 페이지 도달\n")
      return book_datas
    else:
      print("[페이지 이동] 교보 | 다음 페이지")
      driver.execute_script("arguments[0].click();", pages_next)
      # actions.move_to_element(pages_next).click().perform()
      # pages_next.click()
    # print(f"[이전]  " + "  ".join([f"[{p_num.text if "active" in str(p_num.get_attribute("class")).split(" ") else ("{" + p_num.text + "}")}]" for p_num in pages_nums]) + f"  [다음]")\
  print("\n[종료] 교보 크롤링\n")
  return book_datas
