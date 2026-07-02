// 데이터베이스 선택 및 생성
use("AIdb")

// db: AIdb
// students: 컬렉션(컬렉션이 없으면 생성하면서 삽입)
// insertOne(): 문서를 1개 넣는 메서드
db.students.insertOne({
  userId: "apple",
  name: "김사과",
  age: 20,
  major: "AI",
  score: 88
})


// insertMany(): 여러 문서를 한번에 넣음
use("AIdb")
db.students.insertMany([
  { name: "김사과", age: 20, major: "AI", score: 88 },
  { name: "바나나", age: 23, major: "DevOps", score: 98 },
  { name: "오렌지", age: 25, major: "Web", score: 92 },
])


// 전체 조회
// find(): 문서를 조회하는 기본 메서드
// {}: 조건이 없다는 뜻
use("AIdb")
db.students.find({})

/*
    ObjectId
    - 각 문서의 12 바이트(24자리 16진수) 고유한 아이디로 사용되는 데이터 타입
    - SQL의 기본키와 비슷한 역할을 함
    - 각 문서에 _id 필드를 기본적으로 생성하며, 특별히 지정하지 않으면 자동으로 ObjectId 형태로 생성
*/

db.students.find({ name: "김사과" })
// 점수가 80점 이상인 학생 조회
use("AIdb")
db.students.find({ score: { $gte: 60 }})

use("AIdb")
db.students.find({ age: { $gt: 20 }})

use("AIdb")
db.students.find({}, { name: 1, age: 1, _id: 0 })

use("AIdb")
db.students.find({}).sort({ score: 1 })

// 개수 세기
use("AIdb")
db.students.countDocuments({ score: { $gte: 90 }})

use("AIdb")
db.students.updateOne(
  { name: "김사과" },
  { $set: { score: 95 }}
)

use("AIdb")
db.students.updateMany(
  { major: "AI" },
  { $set: { major: "Artificial intelligence" }}
)

use("AIdb")
db.students.find({})