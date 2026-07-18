import app from "./app/app.ts"

app.listen(8092, "127.0.0.1", () => {
  console.log("[main.ts] http://127.0.0.1:8092")
})