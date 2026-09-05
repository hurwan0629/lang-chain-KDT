import secrets
import urllib.parse
import webbrowser

CLIENT_ID = "b084a17b-78b7-4bcd-812e-09a1136d6d18"

REDIRECT_URI = "http://localhost:3000/callback"

BASE_URL = "https://testapi.openbanking.or.kr"

state = secrets.token_hex(16) # 랜덤 문자열 생성

print("state:", state)
print()

params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "redirect_url": REDIRECT_URI,
    "scope": "login inquiry transfer",
    "state": state,
    "auth_type": "0"
}

print("params:", params)
print()

url = (
    f"{BASE_URL}/oauth/2.0/authorize?"
    + urllib.parse.urlencode(params)
)


print("url:", url)
print()

webbrowser.open(url)