const user: User = {
  id: 123,
  name: "hurwan",
  createdAt: new Date()
}

const me: User = {
  id: 123,
  name: "hurwan",
  createdAt: new Date()
}
const myCar: Tesla = new Tesla("V8", me)

myCar.move("forward")
myCar.showInfo()