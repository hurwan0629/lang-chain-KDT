/*
  모듈
  - 자바스크립트 모듈은 코드의 재사용성과 유지보수성을 높이기 위해 기능을 개별 파일로 분리하여 사용할 수 있도록 해주는 구조

  1. CommonJS 방식의 모듈

    let count = 0
    function increase() {
      count++
    }
    function getCount() {
      return count
    }

    module.exports.getCount = getCount 
    module.exports.increase = increase


  2. ESM 방식의 모듈
    // counter.mjs
    export function increase() {
      count++
    }
    export function getCount() {
      return count
    }

    // main.mjs
    import { increase, getCount } from "./counter.mjs"

    increase()
    console.log(getCount())


  라우트
  웹 애플리케이션에서 클라이언트가 요청한 URL 경로와 HTTP 메서드에 따라 서버가 어떤 동작을 수행할지를 정의한느 규칙

    app.route("/경로")
      .get((req, res) => {
        // get 요청 처리  
      })
      .post((req, res) => {
        // post 요청 처리  
      })
      .put((req, res) => {
        // put 요청 처리  
      })
  
  status: 서버가 요청 결과를 어떤 상태로 처리했는지 알려주는 번호
    - 1xx: 요청 처리 중 (거의 사용 안함)
    - 2xx: 성공
      - 200: OK
      - 201: Created
    - 3xx: 다른 주소로 이동
      - 301: 주소가 영구히 변경됨
      - 302: 다른 주소로 가라
    - 4xx: 사용자 요청 문제
      - 401: 인증되지 않은 사용자
      - 403: 권한이 없는 사용자
      - 404: 존재하지 않는 자원
    - 5xx: 서버 문제
      - 500: 서버 오류
*/