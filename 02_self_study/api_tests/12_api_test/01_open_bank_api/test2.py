## 금감원 open_bank에서 아직 좀 걸릴 수 있다고 하여 의사코딩을 작성중입니다.
# 우리 서비스의 한 사용자
import requests

user = {
    "id": 1,
    "name": "A"
}

# 현재는 우리 서비스의 회원이기만 하고 은행 연결정보는 존재하지 않음

# 2. 사용자가 계좌 연결을 누름
def get_openbanking_auth_url():
    return "오픈뱅킹 OAuth authorize URL..."

# A가 우리 서비스에서 제공하는 오픈뱅킹 인증/계좌등록 화면에서 직접 내 계좌를 선택해서
# 동의함 -> 등록되어있는 callback_url[http://localhost:3000/callback]
# 로 ?code=ABC1234&state=... 식으로 응답이 돌아옴
# 그러면 우리 서버에서 { code, state, ... } 을 받는 형태가 됨

# 우리 서버에서 받은 {code}를 오픈뱅킹 Token Server -> access_token으로 교환

def get_callback(code, state):
    # 받은 code와 state를 통해 open_banking 서버에 사용자의
    # { access_token, refresh_token, user_seq_no } 를 받음
    pass

def get_user_bank_account(access_token):
    # access_token을 이용해서
    # 사용자의 bank_account를 받음
    # { bank_name, fintech_use_num } 등이 들어옴
    pass

# 사용자의 bank_account 등을 저장해놓게 된다면
# 이제는 실제 은행 계죄 데이터를 가져오는 단계

def get_user_bank_info(
        access_token, bank_tran_id, fintech_use_num, tran_dtime):
    # GET /v2.0/account/balance/fin_num
    # 를 이용해서
    url = (
        "https://openapi.openbanking.or.kr"
        "/v2.0/account/balance/fin_num"
    )

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "bank_tran_id": bank_tran_id,
        "fintech_use_num": fintech_use_num,
        "tran_dtime": tran_dtime
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    # 이렇게 하면 응답으로
    # {
    #   bank_name
    #   fintech_use_num
    #   balance_amt
    #   available_amt
    #   product_name
    # }

    pass

