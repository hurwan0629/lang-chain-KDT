import requests

url = "https://safemap.go.kr/openapi2/IF_0039"

params = {
    "serviceKey": "",
    "pageNo": 1,
    "numOfRows": 10,
    "returnType": "json",
}

response = requests.get(url, params=params)

print(response.status_code)
print(response.text)