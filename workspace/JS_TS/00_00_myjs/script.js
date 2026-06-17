const moveableArea = document.querySelector(".player-movable");
const player = document.querySelector(".player");

const speed = 15; // px

let x=0, y=0;


document.addEventListener("keydown", (e) => {
  const movableSpaceRect = moveableArea.getBoundingClientRect();
  const playerRect = player.getBoundingClientRect();


  if (e.key === "ArrowRight") {
    console.log("1")
    x += speed;
  }
  if (e.key === "ArrowLeft") {
    console.log("2")
    x -= speed;
  }
  if (e.key === "ArrowDown") {
    console.log("3")
    y += speed;
  }
  if (e.key === "ArrowUp") {
    console.log("4")
    y -= speed;
  }

  const maxX = movableSpaceRect.width - playerRect.width;
  const maxY = movableSpaceRect.height - playerRect.height;

  // console.log(`${minX} ${maxX} ${minY} ${maxY}`)

  x = Math.max(0, Math.min(x, maxX));
  y = Math.max(0, Math.min(y, maxY));

  console.log(`${x}, ${y}`)

  player.style.transform = `translate(${x}px, ${y}px)`;
})