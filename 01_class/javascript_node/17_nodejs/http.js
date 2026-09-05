/*
  http 모듈
  - 웹 서버를 만들 수 있게 해주는 핵심 내장 모듈
  - 클라이언트의 요청을 받고 응답을 반환하는 기능을 제공

  Content-Type
  - 서버가 브라우저에게 "지금 보내는 데이터의 형식이 무엇인지 알려주는 HTTP 헤더"
  - 브라우저는 이 값을 보고 데이터를 어떻게 해석할지 결정

  text/html : html 문서
  text/plain : 일반 텍스트
  application/json : JSON 데이터
  text/css : css 파일
  application/javascript : JavaScript 파일
  image/png : PNG 이미지
  image/jpeg : JPG 이미지
  multipart/form-data : 파일 업로드

  Header
  - 인터넷에서 데이터를 주고 받을 떄 본문(내용))보다 먼저 전달되는 추가 정보 영역으로, "이 데이터가 무엇인지, 어떻게 처리해야 하는지"를 설명해주는 안내문과 같음
  - 브라우저가 서버에 요청을 보낼 때는 어떤 형식을 원하는지, 로그인 정보가 있는지 같은 정보를 헤더에 담고, 서버는 응답할 때 데이터 형식이 무엇인지, 캐시 여부는 어떤지 등의 정보를 헤더에 담아 전달
*/

const http = require("http")

const server = http.createServer((req, res) => {
  res.writeHead(200, {"Content-Type": "text/html"})
  res.end(`
    <!DOCTYPE html>

<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>나를 소개합니다</title>

  <style>
    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: "Pretendard", "Noto Sans KR", Arial, sans-serif;
      background: linear-gradient(135deg, #e0f2fe, #f8fafc);
      color: #1e293b;
      line-height: 1.6;
    }

    .container {
      max-width: 900px;
      margin: 60px auto;
      padding: 30px;
    }

    .profile-card {
      background: white;
      border-radius: 24px;
      padding: 40px;
      box-shadow: 0 20px 40px rgba(15, 23, 42, 0.12);
      text-align: center;
    }

    .profile-img {
      width: 140px;
      height: 140px;
      border-radius: 50%;
      background: #bfdbfe;
      margin: 0 auto 24px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 48px;
      font-weight: bold;
      color: #2563eb;
    }

    h1 {
      font-size: 36px;
      margin-bottom: 10px;
    }

    .subtitle {
      font-size: 18px;
      color: #64748b;
      margin-bottom: 28px;
    }

    .intro {
      font-size: 17px;
      margin-bottom: 36px;
    }

    .section {
      text-align: left;
      margin-top: 32px;
    }

    .section h2 {
      font-size: 22px;
      margin-bottom: 14px;
      color: #2563eb;
    }

    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .tag {
      background: #dbeafe;
      color: #1d4ed8;
      padding: 8px 14px;
      border-radius: 999px;
      font-size: 14px;
      font-weight: 600;
    }

    ul {
      padding-left: 20px;
    }

    li {
      margin-bottom: 8px;
    }

    .contact {
      margin-top: 36px;
      padding: 20px;
      background: #f1f5f9;
      border-radius: 16px;
    }

    .contact a {
      color: #2563eb;
      text-decoration: none;
      font-weight: bold;
    }

    .contact a:hover {
      text-decoration: underline;
    }

    footer {
      margin-top: 30px;
      text-align: center;
      color: #94a3b8;
      font-size: 14px;
    }

    @media (max-width: 600px) {
      .container {
        margin: 30px auto;
        padding: 18px;
      }

      .profile-card {
        padding: 28px;
      }

      h1 {
        font-size: 28px;
      }
    }
  </style>

</head>

<body>
  <div class="container">
    <div class="profile-card">
      <div class="profile-img">나</div>
  <h1>안녕하세요, 저는 [이름]입니다.</h1>
  <p class="subtitle">[직업/전공] · [관심 분야] · [사는 지역]</p>

  <p class="intro">
    저는 새로운 것을 배우고 도전하는 것을 좋아하는 사람입니다.
    꼼꼼하게 문제를 해결하고, 사람들과 함께 성장하는 과정을 중요하게 생각합니다.
    현재는 [관심 있는 분야 또는 하고 있는 일]에 집중하고 있습니다.
  </p>

  <div class="section">
    <h2>나의 특징</h2>
    <ul>
      <li>책임감 있게 맡은 일을 끝까지 해냅니다.</li>
      <li>새로운 기술과 아이디어를 배우는 것을 좋아합니다.</li>
      <li>소통과 협업을 중요하게 생각합니다.</li>
    </ul>
  </div>

  <div class="section">
    <h2>관심 분야</h2>
    <div class="tags">
      <span class="tag">웹 개발</span>
      <span class="tag">디자인</span>
      <span class="tag">프로그래밍</span>
      <span class="tag">문제 해결</span>
      <span class="tag">자기계발</span>
    </div>
  </div>

  <div class="section">
    <h2>목표</h2>
    <p>
      저의 목표는 꾸준히 성장하며 사람들에게 도움이 되는 결과물을 만드는 것입니다.
      앞으로도 다양한 경험을 통해 더 넓은 시야와 실력을 갖춘 사람이 되고 싶습니다.
    </p>
  </div>

  <div class="contact">
    <p>📧 이메일: <a href="mailto:example@email.com">example@email.com</a></p>
    <p>🌐 블로그/포트폴리오: <a href="#">https://my-portfolio.com</a></p>
  </div>
</div>

<footer>
  © 2026 [이름]. All rights reserved.
</footer>
  </div>
</body>
</html>
    `)
})

server.listen(8090, "0.0.0.0", () => {
  console.log("서버 실행 중...")
})