import requests
from bs4 import BeautifulSoup # lxml # aiohttp # httpx # pd.read_html
from pathlib import Path

import os
from urllib.parse import urljoin

# 프레임워크 Scrapy


def first():
  def get_html(url):
    res = requests.request("get", url=url)

    return res

  res = get_html("https://www.naver.com")

  soup = BeautifulSoup(res.text, "html.parser")
  data = soup.prettify()

  path = Path("./text.html")

  with open(path, "w", encoding="utf-8") as f:
    f.write(data)

def second():
  # 가상 서버 주소
  url = "http://127.0.0.1:3000/workspace/python/1_web_crawling/index.html"

  # 서버에 요청 보내기
  response = requests.get(url)

  # HTML 코드 가져오기
  html = response.text

    # HTML 분석
  soup = BeautifulSoup(html, "html.parser")

  # 부모 태그(div) 가져오기
  div = soup.find("div")

  # 자식 태그 가져오기
  news_title = div.find("h1").text
  news_content = div.find("p").text

  # 출력
  print("제목:", news_title)
  print("내용:", news_content)

def third():
  url = "http://127.0.0.1:3000/workspace/python/1_web_crawling/1_index.html"

  response = requests.get(url)

  # HTML 코드 가져오기
  html = response.text

    # HTML 분석
  soup = BeautifulSoup(html, "html.parser")

  # img 태그 찾기
  img_tag = soup.find("img")

  # 이미지 주소 가져오기
  img_src = img_tag["src"]

  print(img_tag)
  print(img_src)
  print("\n\n")
  print(img_src.split("/"))
  print(list(filter(lambda x: x.startswith("q="), img_src.split("/")[-1].split("?")[1:]))[0].removeprefix("q="))

  img_res = requests.request("get", url=str(img_src))


  name = ""
  # save_path = os.path.join(f"images/img.png")

  save_path = Path("./img.png")

  with open(save_path, "wb") as file:
    file.write(img_res.content)

if __name__ == "__main__":
  third()