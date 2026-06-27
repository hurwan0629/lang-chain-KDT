function sendSomeBody() {
  fetch("about", {
    "method": "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "someData1": "someData1",
      "someData2": "someData2",
    })
  }).then(res => {
    if(res.ok) {
      console.log(`데이터 받음 ${res.status}`)
      console.log("res.body:", res.body)
      console.log("res.data:", res.data)
      return res.json()
    }
    else {
      throw Error("응답이 없는데요?")
    }
  }).then(data => {
    console.log("데이터", data)
    console.log(`데이터: ${data}`)
  }).catch(e => {
    console.log(`에러 발생: ${e}`)
  })
}