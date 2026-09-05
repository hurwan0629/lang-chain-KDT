const http = require("http")

const PORT = 8090

const server = http.createServer((req, res) => {
  // console.log("req:", JSON.stringify(req, null, 2));
  // console.log("res:", JSON.stringify(res, null, 2))
  // console.log("req:", req.method)
  // console.log("res:", res)

  // first line
  console.log(`${req.httpVersion} 요청을 받음`);
  console.log(`${req.method} ${req.url} HTTP/${req.httpVersion} ${res.statusCode} ${res.statusMessage}`);  
  let body = "<h2>서버 동작중</h2>"

  // req.method는 판별하지 않음 (예시이니까)
  if(req.url == "/auth") {
    giveAuthToken(req, res)
    body += "\n토큰 지급 완료!"
  }
  else if(req.url === "/authCheck") {
    const checkAuthResult = checkAuthToken(req, res)
    console.log(`checkAuthResult: ${checkAuthResult}`)
    if(checkAuthResult) {
      body += "\n인증된 사용자!"
    } else {
      body += "\n인증되지 않은 사용자!"
    }
  }

  res.statusCode = 200;
  
  // 클라이언트에게 이 텍스트를 해석할 방법을 알려줌
  res.setHeader("Content-Type", "text/html; charset=utf-8")
  

  
  
  console.log(res.getHeaders())
  console.log("body:", body)
  
  res.end(body)
})

server.listen(PORT, () => {
  console.log("auth_test 서버 시작")
})

function giveAuthToken(req, res) {
  res.setHeader("Set-Cookie", "asdf=asdf; Max-Age=300; HttpOnly; Path=/; sameSite=Lax")
}

function checkAuthToken(req, res) {
  // const cookies = req.headers?.cookie?.split("; ").map(cookie => {
  //   const kv = cookie.split("=")
  //   return {
  //     [kv[0]]: kv[1]
  //   }
  // })
  console.log("headers:", req.headers)
  console.log("cookie:", req.headers?.cookie)
  try {
    const cookies = Object.fromEntries(
      req.headers?.cookie?.split("; ").map(cookie => {
        const [key, value] = cookie.split("=");
        return [key, value]
      })
    )
    console.log("cookies:", cookies)
    if(!cookies?.userToken) {
      return false
    }
    return true
  }
  catch {
    return false
  }
}