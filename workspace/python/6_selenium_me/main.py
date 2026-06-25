from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import quote, unquote

import time


def init_driver():
  options = Options()
  options.add_argument("--start-maximized")

  driver = webdriver.Chrome(options=options)
  wait = WebDriverWait(driver, 3)
  
  return driver, wait

def melon_crawl_all_songs_by_keyword(keyword):
  MELON_URL = f"https://www.melon.com/search/song/index.htm?q={keyword}&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&mwkLogType=T"
  # MELON_URL = f"https://www.melon.com/search/song/index.htm?"

  # params = {
  #   "q": keyword,
  #   "section": "",
  #   "searchGnbYn": "Y",
  #   "kkoSpl": "Y",
  #   "kkoDpType": "",
  #   "mwkLogType": "T#params[q]",
  #   "params%5Bsort%5D": "hit",
  #   "params%5Bsection%5D": "all",
  #   "params%5BsectionId%5D": "",
  #   "params%5BgenreDir%5D": "",
  #   "po": "pageObj",
  #   "startIndex": "1",
  # }

  # # 쿼리 만들기

  # for k, v in params.items():
  #   query = str(k) + "=" + str(v) + "&"

  #   MELON_URL += query
  
  # print(MELON_URL)



  driver, wait = init_driver()

  driver.get(MELON_URL)

  # 마지막 번호 가져오기
  # 맨 오른쪽으로 가는 버튼 누르기
  btn_last = wait.until(
    EC.presence_of_element_located(
      (By.CSS_SELECTOR, "a.btn_last")
    )
  )

  btn_last.click()

  # 숫자 채워지는거 기다리기
  time.sleep(1)

  # 마지막 페이지 번호 뽑기
  # last_num = wait.until(
  #   EC.presence_of_element_located(
  #     (By.CSS_SELECTOR, "span.page_num > strong")
  #   )
  # )
  # print(last_num.text)

  # 마지막 검색 결과 번호 보기
  last_num = wait.until(
    EC.presence_of_element_located(
      (By.CSS_SELECTOR, "tbody > tr:last-child > td.no")
    )
  )

  last_num = int(last_num.text)

  page_start_index = [50*a+1 for a in range(0, last_num // 50 + 1)]

  print(page_start_index)
  
  url_format = driver.current_url.replace(f"&startIndex={page_start_index[-1]}", "")

  for psi in page_start_index:
    driver.get(url_format + f"&startIndex={psi}")
    time.sleep(0.5)

    rows = wait.until(
      EC.presence_of_all_elements_located(
        (By.CSS_SELECTOR, "tbody tr")
      )
    )

    for row in rows:
      try:
        print(1)
        cols = row.find_elements(By.TAG_NAME, "td")

        id = cols[1].text
        # 곡명 td
        title_text = cols[2].text.strip()
        title_lines = [
            line.strip()
            for line in title_text.split("\n")
            if line.strip()
        ]

        title = ""
        for line in title_lines:
            if (
                "재생" not in line
                and "담기" not in line
                and "상세정보" not in line
                and not line.startswith("Title")
            ):
                title = line
                break

        print(id)
        print(title)
      except Exception as e:
        print("error")




if __name__ == "__main__":
  melon_crawl_all_songs_by_keyword("안녕하세요")
  # url = "https://www.melon.com/search/song/index.htm?q=%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94&section=&searchGnbYn=Y&kkoSpl=Y&kkoDpType=&mwkLogType=T#params%5Bq%5D=%25EC%2595%2588%25EB%2585%2595%25ED%2595%2598%25EC%2584%25B8%25EC%259A%2594&params%5Bsort%5D=hit&params%5Bsection%5D=all&params%5BsectionId%5D=&params%5BgenreDir%5D=&po=pageObj&startIndex=451"

  # k = url.split("?")[-1].split("&")

  # for a in k:
  #   r = a.split("=")
  #   print(f"{r[0]}: {unquote(r[1])}")
  # print(unquote())