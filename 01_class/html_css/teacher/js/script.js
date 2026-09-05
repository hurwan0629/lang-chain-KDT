a = "0123908".split("").map((e) => {
  console.log(e)
  return Number(e)
}).filter((e) => e > 3)

console.log(a)