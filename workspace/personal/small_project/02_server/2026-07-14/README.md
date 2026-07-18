# 리눅스 서버 실습

`2026-07-14 07:50:03` 기준 직접 ssh, https, 인증서, 배포, 실제 네트워크 시 발생 가능한 문제, 리눅스 등을 하고싶어서 GPT에게 학습 계획을 제공받았습니다.

```md
좋아. 프로젝트와 분리해서 **작은 서버 하나를 직접 배포하고, 일부러 장애를 만들고, 원인을 찾아 복구하는 과정**으로 공부하면 돼.

# 1. 전체 학습 목차

## Part 0. 실습 환경 만들기

1. Ubuntu Server VM 설치
2. 가상 네트워크 설정
3. 서버 IP 확인
4. Windows에서 서버 접근
5. 장애 발생 시 VM 콘솔로 복구하는 방법

## Part 1. Linux 서버 기본

1. 파일과 디렉터리 구조
2. 사용자와 그룹
3. 파일 권한
4. 프로세스 관리
5. 포트와 소켓 확인
6. 로그 확인
7. 패키지 설치와 서비스 관리

## Part 2. SSH

1. SSH 접속 원리
2. 비밀번호 인증
3. 공개키 인증
4. `authorized_keys`
5. SSH 설정 파일
6. SSH 포트 변경
7. 방화벽과 SSH
8. SSH 오류 분석
9. SSH 보안 설정
10. SCP와 SFTP

## Part 3. HTTP 서버 실행

1. 간단한 Node.js HTTP 서버 작성
2. 서버 프로세스 실행
3. IP 바인딩
4. 포트 개방
5. localhost와 외부 접속 차이
6. HTTP 요청 확인
7. 프로세스 종료와 재실행
8. 환경변수 사용

## Part 4. systemd

1. Linux 서비스 개념
2. 서비스 파일 작성
3. 자동 시작 설정
4. 프로세스 재시작 정책
5. 서비스 사용자 권한
6. 환경변수 전달
7. 로그 확인
8. 서비스 실행 실패 분석

## Part 5. Nginx 리버스 프록시

1. 웹 서버와 애플리케이션 서버 차이
2. Nginx 설치
3. 정적 파일 제공
4. 리버스 프록시 설정
5. Host 및 Proxy 헤더
6. 여러 도메인 처리
7. 502 오류 분석
8. Nginx 로그
9. 설정 파일 검사
10. 무중단 설정 적용

## Part 6. 네트워크와 방화벽

1. 서버 IP와 포트
2. TCP 연결 과정
3. Listen 포트
4. 방화벽 규칙
5. 내부 접근과 외부 접근
6. NAT와 포트 포워딩
7. DNS 이름 해석
8. timeout과 connection refused 차이
9. Windows에서 포트 테스트
10. 패킷 흐름 분석

## Part 7. DNS

1. 도메인과 IP의 관계
2. A, AAAA, CNAME 레코드
3. DNS 캐시
4. 로컬 `hosts` 파일
5. Nginx `server_name`
6. DNS 전파
7. 잘못된 DNS 설정 분석
8. `nslookup`, `dig`

## Part 8. HTTPS와 TLS

1. HTTP와 HTTPS 차이
2. TLS 연결 과정
3. 인증서와 개인키
4. 인증기관
5. 자체 서명 인증서
6. 인증서 도메인 검증
7. 인증서 만료
8. Nginx HTTPS 설정
9. HTTP에서 HTTPS 리다이렉트
10. TLS 오류 분석
11. Let's Encrypt와 Certbot
12. 인증서 자동 갱신

## Part 9. Git을 이용한 서버 배포

1. 서버에서 저장소 clone
2. HTTPS 방식 Git 인증
3. SSH 방식 Git 인증
4. GitHub SSH 키
5. Deploy key
6. 브랜치별 배포
7. `git pull` 충돌
8. 서버 코드 수정 문제
9. 이전 버전으로 롤백
10. 배포 스크립트 작성

## Part 10. Docker 배포

1. 이미지와 컨테이너
2. Dockerfile
3. 포트 매핑
4. 환경변수
5. 볼륨
6. 컨테이너 네트워크
7. 컨테이너 로그
8. 컨테이너 내부 접근
9. Docker Compose
10. Nginx와 Node 컨테이너 연결
11. 컨테이너 재시작 정책
12. Docker 배포 장애 분석

## Part 11. 배포 자동화

1. 수동 배포 과정 정리
2. Bash 배포 스크립트
3. GitHub Actions
4. SSH를 통한 원격 배포
5. GitHub Secrets
6. 빌드 실패 처리
7. 배포 후 상태 검사
8. 실패 시 롤백
9. Blue-Green 배포 개념
10. 무중단 배포 개념

## Part 12. 로그와 장애 분석

1. 애플리케이션 로그
2. Nginx 로그
3. systemd 로그
4. SSH 로그
5. Docker 로그
6. 로그 레벨
7. Health Check
8. 장애 원인 범위 좁히기
9. CPU, 메모리, 디스크 확인
10. 운영 장애 보고서 작성

---

# 2. 실제로 할 작업

전체 과정에서는 하나의 작은 서버를 계속 발전시킨다.

```text
Windows PC
    ↓ SSH / HTTP / HTTPS
Ubuntu Server
    ├─ Nginx
    ├─ Node.js HTTP 서버
    └─ systemd 또는 Docker
```

Node 서버는 복잡하게 만들 필요 없이 다음 기능만 있으면 된다.

```text
GET /
GET /health
GET /env
GET /error
```

예를 들면:

* `/` : 정상 응답
* `/health` : 서버 상태 반환
* `/env` : 환경변수 확인
* `/error` : 일부러 오류 발생

이 서버를 이용해서 아래 작업들을 반복한다.

---

## 작업 1. Ubuntu 서버 만들기

할 작업:

* Ubuntu Server VM 설치
* 사용자 계정 생성
* 네트워크 어댑터 설정
* 서버 IP 확인
* Windows에서 ping 테스트
* VM 스냅샷 생성

공부할 주제:

* 가상머신
* 게스트 OS와 호스트 OS
* NAT 네트워크
* 브리지 네트워크
* 사설 IP
* DHCP
* 네트워크 인터페이스

---

## 작업 2. SSH 접속 만들기

할 작업:

```bash
ssh user@서버IP
```

이후 SSH 키 로그인으로 변경한다.

```bash
ssh-keygen
ssh-copy-id user@서버IP
```

일부러 발생시킬 장애:

* 잘못된 IP
* 잘못된 사용자
* 잘못된 SSH 포트
* SSH 서비스 종료
* 방화벽에서 포트 차단
* 개인키를 잘못 선택
* `authorized_keys` 권한 변경
* 서버 host key 변경

공부할 주제:

* SSH 클라이언트와 서버
* 공개키와 개인키
* 인증과 암호화
* 서버 host key
* `known_hosts`
* `authorized_keys`
* SSH handshake
* timeout
* connection refused
* permission denied

---

## 작업 3. Linux 권한 문제 만들기

할 작업:

* 사용자와 그룹 생성
* 파일 소유권 변경
* 읽기·쓰기·실행 권한 변경
* 서비스 사용자가 파일을 읽지 못하게 만들기
* SSH 키 파일 권한을 잘못 설정하기

사용할 명령:

```bash
ls -l
chmod
chown
id
whoami
groups
namei -l
```

공부할 주제:

* 사용자
* 그룹
* 소유자
* 읽기·쓰기·실행 권한
* 디렉터리 실행 권한
* root
* `sudo`
* 최소 권한 원칙

---

## 작업 4. Node HTTP 서버 실행

할 작업:

* Node.js 설치
* 한 파일짜리 HTTP 서버 작성
* 3000번 포트에서 실행
* `curl`로 요청
* 다른 PC에서 접속
* `127.0.0.1`과 `0.0.0.0` 바인딩 비교

일부러 발생시킬 장애:

* 잘못된 포트로 접속
* 서버 프로세스 종료
* 이미 사용 중인 포트 사용
* localhost에만 바인딩
* 환경변수 누락
* 파일 권한 오류

공부할 주제:

* 프로세스
* PID
* TCP Listen
* IP 바인딩
* loopback
* 포트 충돌
* `EADDRINUSE`
* `EACCES`
* 환경변수

---

## 작업 5. systemd 서비스 만들기

할 작업:

* Node 서버용 서비스 파일 작성
* 서버 부팅 시 자동 실행
* 프로그램 종료 시 자동 재시작
* 서비스 사용자 지정
* 환경변수 파일 연결

일부러 발생시킬 장애:

* 잘못된 `ExecStart`
* 잘못된 `WorkingDirectory`
* Node 경로 오류
* 서비스 사용자 권한 부족
* 환경변수 누락
* 서비스 파일 변경 후 `daemon-reload` 누락

공부할 주제:

* daemon
* systemd
* unit
* service lifecycle
* 자동 시작
* 재시작 정책
* 표준 출력과 로그
* 실행 사용자

---

## 작업 6. Nginx 연결

할 작업:

```text
브라우저 → Nginx:80 → Node:3000
```

* Nginx 설치
* `/` 요청을 Node로 전달
* 정적 HTML 제공
* Nginx와 Node 로그 분리
* Node 3000번 포트는 외부에서 막기

일부러 발생시킬 장애:

* Node 서버 종료
* Nginx에서 잘못된 포트 지정
* 잘못된 설정 문법
* 중복된 `server_name`
* 설정 파일 활성화 누락
* 파일 권한 문제

공부할 주제:

* 웹 서버
* 애플리케이션 서버
* 리버스 프록시
* upstream
* proxy header
* 502 Bad Gateway
* 404와 502 차이
* access log
* error log

---

## 작업 7. 방화벽 실습

할 작업:

* SSH 22 허용
* HTTP 80 허용
* HTTPS 443 허용
* Node 3000 외부 차단
* 특정 포트만 허용

일부러 발생시킬 장애:

* SSH 차단
* HTTP 차단
* 443만 차단
* 서비스는 실행 중인데 방화벽에서 차단
* 방화벽은 열려 있지만 서비스가 없는 상태 만들기

공부할 주제:

* 인바운드
* 아웃바운드
* 포트 개방
* 방화벽
* Listen 상태
* timeout
* connection refused
* 서비스 포트와 방화벽 규칙 차이

---

## 작업 8. DNS 실습

처음에는 실제 도메인 없이 Windows `hosts` 파일을 사용한다.

```text
192.168.0.50 study.local
```

할 작업:

* 이름으로 서버 접속
* Nginx `server_name` 설정
* 여러 가상 도메인 만들기
* DNS 캐시 초기화

일부러 발생시킬 장애:

* 잘못된 IP 지정
* 잘못된 도메인 사용
* `www` 유무 차이
* Nginx `server_name` 불일치
* 캐시 때문에 이전 IP로 접속

공부할 주제:

* hostname
* DNS resolver
* hosts 파일
* A 레코드
* CNAME
* TTL
* DNS 캐시
* 가상 호스트

---

## 작업 9. HTTPS 설정

처음에는 자체 서명 인증서를 사용하고, 이후 실제 도메인으로 Let's Encrypt를 사용한다.

할 작업:

* 개인키 생성
* 인증서 생성
* Nginx에 HTTPS 적용
* HTTP 요청을 HTTPS로 리다이렉트
* 인증서 내용 확인

일부러 발생시킬 장애:

* 인증서와 개인키가 맞지 않음
* 인증서 파일 경로 오류
* 인증서 권한 오류
* 인증서 만료
* 도메인 불일치
* 443 포트 차단
* HTTP와 HTTPS 포트 혼동

공부할 주제:

* TLS
* 인증서
* 개인키
* 공개키
* 인증기관
* 인증서 체인
* 도메인 검증
* TLS handshake
* SNI
* 자체 서명 인증서

---

## 작업 10. Git으로 서버 코드 배포

할 작업:

* GitHub에 작은 저장소 생성
* Ubuntu에서 clone
* 코드 수정 후 pull
* SSH 방식으로 private repository 접근
* 배포용 키 생성
* 특정 브랜치 배포
* 이전 커밋으로 롤백

일부러 발생시킬 장애:

* remote URL 오류
* SSH key 미등록
* 잘못된 branch
* 서버에서 파일 수정 후 pull 충돌
* detached HEAD
* `.env` 커밋
* 잘못된 커밋 배포

공부할 주제:

* Git remote
* GitHub 인증
* SSH clone
* HTTPS clone
* deploy key
* branch
* fetch와 pull
* reset
* revert
* rollback

---

## 작업 11. Docker로 변경

할 작업:

* Node 서버 Dockerfile 작성
* 이미지 빌드
* 컨테이너 실행
* 포트 매핑
* 환경변수 전달
* Docker Compose 사용
* Nginx 컨테이너와 Node 컨테이너 연결

일부러 발생시킬 장애:

* 포트 매핑 누락
* 잘못된 Dockerfile 명령
* 실행 명령 오류
* 컨테이너 즉시 종료
* 환경변수 누락
* 컨테이너 내부에서 `localhost` 잘못 사용
* 볼륨으로 파일이 가려지는 문제

공부할 주제:

* 이미지
* 컨테이너
* Dockerfile
* build context
* layer
* port mapping
* volume
* container network
* Docker DNS
* restart policy

---

## 작업 12. 자동 배포 만들기

할 작업:

* 배포 Bash 스크립트 작성
* GitHub Actions에서 테스트 실행
* GitHub Actions에서 서버 SSH 접속
* 코드 pull
* 서비스 재시작
* `/health` 검사
* 실패하면 배포 중단

일부러 발생시킬 장애:

* GitHub Secret 이름 오류
* SSH 개인키 오류
* 서버 host key 문제
* 테스트 실패
* 빌드 실패
* 서비스 재시작 실패
* Health Check 실패
* 새 버전 실패 후 이전 버전 복구

공부할 주제:

* CI
* CD
* workflow
* runner
* secret
* deploy script
* health check
* rollback
* 배포 원자성
* 무중단 배포

---

# 3. 이 과정에서 익혀야 할 핵심 진단 순서

장애가 생기면 아래 순서로 확인한다.

```text
1. 주소와 DNS가 맞는가?
2. 서버까지 네트워크 연결이 가능한가?
3. 방화벽이 포트를 허용하는가?
4. 프로그램이 해당 포트를 Listen 중인가?
5. 프로세스가 정상 실행 중인가?
6. Nginx가 올바른 서버로 전달하는가?
7. 파일과 실행 사용자 권한이 맞는가?
8. 환경변수와 설정값이 맞는가?
9. 애플리케이션 자체에 오류가 있는가?
10. 로그에 어떤 기록이 남았는가?
```

목표는 단순히 SSH, HTTPS, Docker 명령어를 외우는 것이 아니라, 오류가 발생했을 때 **어느 계층의 문제인지 구분하는 능력**을 만드는 것이다.
```