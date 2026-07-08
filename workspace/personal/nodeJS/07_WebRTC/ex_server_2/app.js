import express from "express"
import { fileURLToPath } from "url"
import path from "path"

const app = express()

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

app.use(express.static(path.join(__dirname, "resource")))

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "resource", "pages", "index.html"))
})

app.get("/communicate", (req, res) => {
  res.sendFile(path.join(__dirname, "resource", "pages", "communicate.html"))
})

export default app