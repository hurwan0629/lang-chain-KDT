function fetch_submit() {
  fetch("/submit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      name: "이름",
      content: "내용"
    })
  }).then(response => {
    if(!response.ok) {
      document.getElementById("result").value = "요청이 실패했습니다."
      throw new Error('네트워크 응답에 문제가 있습니다.');
    }
    return response.json()
  }).then(data => {
    console.log(data.message)
    document.getElementById("result").textContent = data.message
  }).catch(e => {
    console.log(e)
  })
}