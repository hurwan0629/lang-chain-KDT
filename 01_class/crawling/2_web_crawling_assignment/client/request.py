import requests
from bs4 import BeautifulSoup
from pathlib import Path

def get_html_as_bs(url):
  res = requests.request("get", url)
  html = res.content

  soup = BeautifulSoup(html, "html.parser")
  return soup

if __name__=="__main__":
  pass
  result = get_html_as_bs("https://basicenglishspeaking.com/daily-english-conversation-topics/")
  dir = Path(__file__) / ".."
  with open(dir / "page.html", "w") as f:
    f.write(result.prettify())

  path = Path(__file__).resolve().parent
  print(path)
