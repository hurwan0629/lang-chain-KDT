# GPT API 기반 AI 광고 문구 생성 서비스 구현

> 과제 요구사항
```md
1. 프로젝트 구성
- Gradio 클라이언트
- FastAPI 서버

2. Gradio 화면 구현
- 제품 이름 입력창
- 제품 주요 내용 입력창
- 광고 문구의 느낌을 선택하는 체크박스 그룹(재밌게, 과장스럽게, 참신하게, 고급스럽게, 센스있게, 신선하게, 전문성있게..)
- 광고 문구 생성 버튼
- 생성된 광고 문구 출력창
- MongoDB에 저장된 최근 광고 문구 목록

3. FastAPI 요청 모델 구현
- product_name
- details
- tone_and_manner

4. GPT API 광고 문구 생성
- 제품이름, 제품 주요 내용, 광고 문구 스타일의 정보가 모델에 전달되어야 함
- 생성되는 광고 문구는 한 문장으로 작성되어야 하며, 설명이나 제목 없이 광고 문구만 반환되도록 지시문을 작성

5. MongoDB 저장
- 생성된 광고 문구와 입력 데이터를 MongoDB에 저장
- 제품 이름, 제품 주요 내용, 광고 문구의 느낌, 생성된 광고 문구 저장

6. 최신 데이터 조회
- 광고 문구 생성이 완료되면 MongoDB에 저장된 데이터를 최신순으로 조회

    {
        "ad": "생성된 광고 문구",
        "datas": [
            {
                "product_name": "제품 이름",
                "details": "제품 주요 내용",
                "tone_and_manner": "광고 문구 스타일",
                "ad": "생성된 광고 문구"
            }
        ],
        ...
    }
```

---

## API 명세서

> 단 2개의 api만 존재. [생성+저장, 불러오기]

### GET /datas
> 응답 [최신순]
```json
{
    "datas": [
      {
        "user_req": {
          "product_name": "제품 이름",
          "details": "제품 주요 내용",
          "tone_and_manner": "광고 문구 스타일"
        },
        "server_res": {
          "ad": "생성된 광고 문구",
          "created_at": "DateISOString-UTF"
        }
      }
    ]
}
```


### POST /content
> 요청 body (인증 없음)
```json
{
  "product_name": "제품 이름",
  "details": "제품 주요 내용",
  "tone_and_manner": "광고 문구 스타일"
}
```

> 응답

```json
{
    "data": {
        "user_req": {
          "product_name": "제품 이름",
          "details": "제품 주요 내용",
          "tone_and_manner": "광고 문구 스타일"
        },
        "server_res": {
          "ad": "생성된 광고 문구",
          "created_at": "DateISOString-UTF"
        }
      }
}
```

---

## DataBase (MongoDB)
> collection: `contents`
> index: `created_at` [정렬 비용]
```json
{
  "user_req": {
    "product_name": "제품 이름",
    "details": "제품 주요 내용",
    "tone_and_manner": "광고 문구 스타일"
  },
  "server_res": {
    "ad": "생성된 광고 문구",
    "created_at": "DateISOString-UTF"
  }
}
```

---

## OpenAI API 프롬프트 설정

