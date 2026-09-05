const addTodoButton = document.getElementById("addBtn")
const userTodoInput = document.getElementById("todoInput")
const todoList = document.getElementById("todolist")

const listTotal = document.getElementById("totalCount")
const listRemain = document.getElementById("remainingCount")

const updateModal = document.getElementById("update-modal")

let listTotalCount;
let listRemainCount;

let todoData;

window.onload = function() {
  console.log("window.onload")

  const savedTodo = localStorage.getItem('userTodo')
  
  todoData = savedTodo ? JSON.parse(savedTodo) : []

  console.log(todoData)
  
  listTotalCount = 0
  listRemainCount = 0

  initMeta()

  todoData.forEach(element => {
    console.log(todoData)
    addTodoList(element.content, element.finished)
  })
}



function initMeta() {
  listTotal.textContent = listTotalCount
  listRemain.textContent = listRemainCount
}

function addTodoData(content) {
  console.log(content)
  todoData.push({"content": content, "finished": false})

  localStorage.setItem('userTodo', JSON.stringify(todoData))
}

function finishTodo(num, newList) {
  if(!todoData[num]) {
    alert('존재하지 않는 todo입니다!')
    return
  }
  todoData[num]["finished"] = true
  localStorage.setItem('userTodo', JSON.stringify(todoData))

  listRemainCount -= 1

  initMeta()

  newList.classList.add('finished')
}

function addTodoList(content, finished=false) {
  console.log(`addTodoList(${content}, ${finished})`)
  if(!content) {
    console.log("2. 입력 공간 비어있음")
    return
  }
  console.log("할일:", content)

  const newList = document.createElement('li')
  newList.dataset.key = ++listTotalCount

  if(!finished) {
    listRemainCount += 1
  }

  newList.innerHTML = `
    <p>${String(listTotalCount)}. ${content}</p>
    <div class="todo-buttons">
      <button type='button' id="todo-${listTotalCount}" ${finished ? 'disabled' : ''}>종료</button>
      <button type='button' id="todo-update-${listTotalCount-1}">수정</update>
      <button type='button' id="todo-delete-${listTotalCount-1}" 
            class="delete-todo">삭제</button>
    </div>
  `

  if(finished) {
    newList.classList.add('finished')
  }
  else {
    const finishButton = newList.querySelector(`#todo-${listTotalCount}`)
  
    finishButton.addEventListener("click", () => {
      finishTodo(listTotalCount-1, newList)
      finishButton.disabled = true
    })
  }

  const deleteButton = newList.querySelector(`#todo-delete-${listTotalCount-1}`)
  deleteButton.addEventListener("click", () => {
    todoData.splice(listTotalCount-1, 1)
    localStorage.setItem('userTodo', JSON.stringify(todoData))
    window.location.reload();
  })
  
  // const updateButton = newList.querySelector(`#todo-update-${listTotalCount-1}`)
  // updateButton.addEventListener("click", () => {
  //   newList. = getContentToUpdate()
  // })

  
  todoList.prepend(newList)

  // 메타데이터 초기화하기
  initMeta()
}


addTodoButton.addEventListener("click", () => {
  console.log("1. 할일 추가 버튼 눌림")
  addTodoData(userTodoInput.value.trim())
  addTodoList(userTodoInput.value.trim())
  userTodoInput.value = ""
  console.log(todoData)
})

userTodoInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    addTodoButton.click()
  }
})

// function getContentToUpdate() {
//   updateModal.hidden = false
  


// }