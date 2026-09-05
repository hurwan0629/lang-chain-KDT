const memoInput = document.getElementById("memoInput")
const addBtn = document.getElementById("addBtn")
const memoList = document.getElementById("memList")

loadMemos()

async function loadMemos() {
  try{
    const response = await fetch("/memos", {
        method: "GET",
        headers: {
          "Content-Type": "application/json"
        },  
      })
    
    const data = await response.json()

    if(data.success){
      const memos = data?.memos

      renderMemos(memos)
    } else {
      throw new Error("요청이 실패했습니다..")
    }

    

  } catch(err) {
    console.log("에러 발생:", err)
  }
}

function renderMemos(memos) {
  memoList.innerHTML = ""

  memos.forEach((memo, index) => {
    const li = document.createElement("li")
    li.className = "memo-item"
    li.key = index
    li.innerHTML = `
    <div key=${memo._id}>
      <span>${memo.text}</span>
      <div class="memo-buttons">
        <button onclick="editMemo('${memo._id}')">수정</button>
        <button onclick="deleteMemo('${memo._id}')">삭제</button>
      </div>
    </div>
    `

    memoList.appendChild(li)
  })
}

function deleteMemo(memoId) {
  console.log("deleteMemo: ", memoId)
  const check = confirm("정말 삭제하시겠습니까?")
  // console.log(check)

  fetch(`/memo/${memoId}`, {
    method: "DELETE",
  }).then((res) => {
    if(!res.ok) {
      console.log("에러 발생")
      throw new Error("에러 발생")
    } else if (res.status === 204) {
      console.log("삭제 완료!")
      alert("삭제 완료!")
      loadMemos()
      return
    }
  }).catch(err => {
    alert("요청이 실패하였습니다!")
  })

}

async function editMemo(memoId) {
  const input = prompt("수정할 내용을 입력하세요")

  console.log(`\n --- input --- \n`)
  console.log(input)
  console.log(!input.trim())
  if(!input.trim()) {
    alert("내용이 입력되지 않았습니다.")
  }

  const res = await fetch(`/memos/${memoId}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: input })
  })

  console.log("res status:", res?.status)

  if(!res.ok) {
    alert("수정이 실패하였습니다!")
  }
  else {
    alert("수정 성공!")
    loadMemos()
  }
}

addBtn.addEventListener("click", async() => {
  const text = memoInput.value.trim()
  if(!text) {
    alert("메모를 입력하세요")
    return
  }

  try {
    const response = await fetch("/memo", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text })
    })

    const data = await response.json()

    memoInput.value = ""

    loadMemos(data.memos)
  } catch (err) {
    console.log("에러 발생:", err)
  }
})