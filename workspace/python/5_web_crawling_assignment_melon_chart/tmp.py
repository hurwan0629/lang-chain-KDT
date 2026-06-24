import requests


_headers_02 = {
    "User-Agent": (
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
      "AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
  }

print(
  requests.request(
    "GET",
    "https://www.melon.com/commonlike/getSongLike.json?contsIds=602024048"
  )
)




# 2xx - 성공
# 3xx - 권한 문제
# 4xx - 데이터 없음? 
