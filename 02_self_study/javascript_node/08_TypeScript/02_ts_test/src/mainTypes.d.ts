type DateType = Date
type User = {
  id: number,
  name: string,
  createdAt: DateType
}

interface Car {
  engine: string,
  owner: User,
  move(direction: string): void
}

class Tesla implements Car {
  engine: string
  owner: User

  constructor(engine: string, owner: User) {
    this.engine = engine
    this.owner = owner
  }

  move(direction: string): void {
    console.log("going to", direction)
  }

  showInfo() {
    console.log(`
engine: ${this.engine}
owner: ${JSON.stringify(this.owner)}`)
  }
}