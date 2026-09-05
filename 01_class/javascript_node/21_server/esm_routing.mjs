import express from "express"

const app = express()

app.route("/posts")
    .get((req, res) => {
      res.status(200).send("<h1>GET /posts </h1>")
    })
    .post((req, res) => {
      res.status(200).send("<h1>POST /posts </h1>")
    })
    .put((req, res) => {
      res.status(200).send("<h1>PUT /posts </h1>")
    })
    .delete((req, res) => {
      res.status(200).send("<h1>DELETE /posts </h1>")
    })

app.listen(8091, () => {
  console.log("서버 실행 시작")
})