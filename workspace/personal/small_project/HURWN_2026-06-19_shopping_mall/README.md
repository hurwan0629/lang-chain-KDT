# 요구조건 정의
제목: 미니 온라인 스토어

사용 스택: Python과 MySQL

### 유저플로우 
- (page) 메인페이지
  - (button) 1. 회원 가입
    - (page) 회원 가입 포멧
      - 아이디, 비밀번호, 비밀번호 확인, 이름, 이메일 입력
      - 아이디, 이메일 중복 불가
      - 생성 시 저장후 메시지 출력
    - (button) 메인 페이지로 나가기 (0)
  - (button) 2. 로그인
    - 로그인 실패 시 
      - 실패 메시지 출력
      - 재입력 요구
    - 로그인 성공 시 
      - (page) 메인 페이지
        - (button) 상품 목록 조회
          - (page) 모든 상품을 표 형태로 출력 (상품Id, 상품명, 가격, 재고) (재고가 0이면 품절 표시)
        - (button) 상품 검색
          - (page) 상품명 키워드로 검색. 검색 결과는 상품 목록 조회와 동일하게 제공. (결과 없으면 "검색 결과 없음" 출력)
        - (button) 주문하기
          - (page) 사용자가 원하는 상품ID와 수량 입력 -> 재고 여부 검사 -> 부족하면 거부 및 안내메시지 -> 충분하면 총 금액 알려주고 최종 결제 여부 묻기 -> 
            - (추가 점수 부여. 트랜잭션을 사용하지 않아도 감점하지 않음) 
            - order_header에 주문 기본 정보를 저장
            - order_item에 상품별 주문 상세 정보를 저장
            - product.stock에서 주문 수량만큼 차감
            - 모든 작업이 성공하면 커밋하고, 처리 중 오류 발생 시 모든 변경 사항을 롤백해야 한다.
            - 
        - (button) 주문 내역 조회
          - (page)  주문번호, 총금액, 상태, 주문일자
            - 특정 주문 선택하면 주문 상세정보 출력
              - (page) 상품명, 수량, 가격(스냅샷), 총 금액, 상태, 결제 여부

        - (button) 로그아웃 
          - (action) 메인 페이지로 이동 (break)
  - (button) 0. 프로그램 종료
### 설계 요구사항
- Python 3.x
- CLI 형태
- MySQL 사용
- 모듈 사용 
- 예외 처리
- 로그인 

# Page

- 화면
  - 기본 실행 파일
  - 로그인 화면
    - 실행 파일
    - 메인 화면
      - 실행 파일
      - 상품 목록 화면
      - 상품 검색 화면
        - 실행 파일
      - 주문 목록 화면
        - 실행 파일
        - 주문 상세 화면
          - 실행 파일
      - 주문 화면
  - 회원가입 화면
    - 실행 파일

# Service
아이디 중복 확인: check_id_duplicated(id: str) -> bool

`selct 1 from member where id = %s, (id, )`

이메일 중복 확인: check_email_duplicated(email, str) -> bool
`selct 1 from member where email = %s, (email ,)`

회원가입: regist_user(id, password, name, email)
`insert into member (id, password, name, email) values (%s, %s, %s, %s), (id, password, name, email)`
로그인: service.try_login(username, password) -> UserLoginDTO

# 페이지 제약
사용자 아이디는 8 ~ 90
사용자 비번은 8 ~ 20
사용자 이름은 2 ~ 20
이메일 길이는 20 ~ 90

# TODO
[x] 회원가입
[x] 로그인
[] 상품 목록 조회
[] 상품 검색
[] 주문하기
[] 주문 내역 조회
[] 로그아웃
[] 프로그램 종료
