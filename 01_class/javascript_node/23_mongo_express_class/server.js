const express = require("express")
const path = require("path")
const { MongoClient, ObjectId } = require("mongodb")
const morgan = require("morgan")
require("dotenv").config()

const uri = process.env.MONGO_URI;
const dbName = process.env.DB_NAME;

const app = express()
const PORT = 8091
app.use(express.json())
app.use(express.static(path.join(__dirname, "public")))
app.use(morgan("dev"))

const client = new MongoClient(uri)

let db;

let class_memo;

async function startServer() {
  try {
    await client.connect()
    console.log("연결 성공")

    db = client.db(dbName)
    // console.log("db 연결!", db)

    class_memo = await db.collection("class_memo")
    console.log("컬렉션 연결 성공!")

    
  } catch (err) {
    console.error(err)
  }
}

app.get("/memos", async(req, res) => {
    try {
        const { keyword } = req.query
        let filter = {}

        if(keyword && keyword.trim() !== "") {
          filter = {
            text: { $regex: keyword.trim(), $options: "i" }
          }
        }

        const memos = await class_memo.find(filter)
                  .sort({ createdAt: -1 }).toArray()
        res.status(200).json({
          success: true,
          count: memos.length,
          memos
        })
    } catch(error) {
      console.log(error)
      res.status(500).json({
          success: true,
          message: "메모 조회중 오류가 발생!"
        })
    }
})

app.post("/memo", async(req, res) => {
  try {

    
    // console.log(await class_memo.find({}).toArray())

    const { text } = req.body
    if(!text || text.trim() === "") {
      return res.status(400).json({
        success: false,
        message: "메모 내용을 입력해주세요"
      })
    }

    const newMemo = {
      text: text.trim(),
      createAt: new Date()
    }

    await class_memo.insertOne(newMemo)
    return res.status(200).json({
        success: true,
        message: "메모가 추가되었습니다."
    })

  } catch(err) {
    console.error("메모 저장 오류:", err)
    return res.status(500).json({
        success: false,
        message: "서버에 오류가 있습니다."
      })
  }
})

app.put("/memos/:id", async (req, res) => {
  try{
    const { id } = req.params
    const { text } = req.body
    // id가 MongoDB ObjectId 형식인지 검사하고 아니면 400에러를 반환
    if(!ObjectId.isValid(id)) {
        return res.status(400).json({
            success: false,
            message: "올바르지 않은 메모 id 형식!!"
        })
    }

    if(!text || text.trim() === "") {
        return res.status(400).json({
            success: false,
            message: "변경할 메모 내용을 입력해주세요"
        })
    }

    const result = await class_memo.findOneAndUpdate(
      { _id: new ObjectId(id) },
      {
        $set: {
          text: text.trim(),
          updatedAt: new Date()
        }
      },
      {
        returnDocument: "after"
      }
    )

    if(!result) {
      return res.status(400).json({
          success: false,
          message: "해당 id의 메모를 찾을 수 없습니다."
      })
    }

    res.status(200).json({
      success: true,
      message: "메모가 수집되었습니다. (PUT)",
      memo: result
    })

  }catch(error){
    console.log("메모 수정중 오류:", error)
    return res.status(500).json({
            success: false,
            message: "서버 에러"
        })
  }
})

app.delete("/memo/:id", async(req, res) => {
  console.log("DELETE /memo")
  const { id } = req.params
  console.log(id)
  try {
    // 형식 체크
    if(!ObjectId.isValid(id)) {
      console.log("형식 오류")
      return res.status(400).json({
        success: false,
        message: "해당 id의 메모를 찾을 수 없습니다."
      })
    }

    // 삭제
    console.log("데이터 삭제 시도")
    const deleteResult = await class_memo.deleteOne({ _id: new ObjectId(id) })
    console.log("result:", deleteResult)
    return res.status(204).end()
    // .json({
    //   success: true,
    //   message: "데이터를 성공적으로 삭제했습니다."
    // })
  } catch (err) {
    console.log("[app.delete /memo/:id]:", err)
    res.status(500).json({
      success: false,
      message: "삭제 처리중 오류가 발생했습니다."
    }) 
  }
})

app.listen(PORT, () => {
  startServer()
})