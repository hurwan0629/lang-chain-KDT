const slides = Array.from(document.querySelectorAll(".slide"));
const previousButton = document.querySelector("#prevButton");
const nextButton = document.querySelector("#nextButton");
const fullscreenButton = document.querySelector("#fullscreenButton");
const pageIndicator = document.querySelector("#pageIndicator");
const progressBar = document.querySelector("#progressBar");

let currentIndex = getInitialIndex();
let touchStartX = null;

function getInitialIndex() {
  const match = window.location.hash.match(/^#slide-(\d+)$/);
  if (!match) return 0;

  const requestedIndex = Number(match[1]) - 1;
  return Math.min(Math.max(requestedIndex, 0), slides.length - 1);
}

function formatNumber(value) {
  return String(value).padStart(2, "0");
}

function render() {
  slides.forEach((slide, index) => {
    const isActive = index === currentIndex;
    slide.classList.toggle("is-active", isActive);
    slide.setAttribute("aria-hidden", String(!isActive));
  });

  previousButton.disabled = currentIndex === 0;
  nextButton.disabled = currentIndex === slides.length - 1;
  pageIndicator.textContent =
    `${formatNumber(currentIndex + 1)} / ${formatNumber(slides.length)}`;
  progressBar.style.width = `${((currentIndex + 1) / slides.length) * 100}%`;

  const hash = `#slide-${currentIndex + 1}`;
  window.history.replaceState(null, "", hash);
  document.title = `${slides[currentIndex].dataset.title} | 기후 위기 의사결정 지원 서비스`;
}

function goTo(index) {
  const nextIndex = Math.min(Math.max(index, 0), slides.length - 1);
  if (nextIndex === currentIndex) return;
  currentIndex = nextIndex;
  render();
}

function next() {
  goTo(currentIndex + 1);
}

function previous() {
  goTo(currentIndex - 1);
}

async function toggleFullscreen() {
  if (!document.fullscreenElement) {
    await document.documentElement.requestFullscreen?.();
  } else {
    await document.exitFullscreen?.();
  }
}

previousButton.addEventListener("click", previous);
nextButton.addEventListener("click", next);
fullscreenButton.addEventListener("click", toggleFullscreen);

document.addEventListener("keydown", (event) => {
  const target = event.target;
  const isInteractive =
    target instanceof HTMLInputElement ||
    target instanceof HTMLTextAreaElement ||
    target instanceof HTMLSelectElement ||
    target?.isContentEditable;

  if (isInteractive) return;

  if (["Enter", " ", "ArrowRight", "ArrowDown", "PageDown"].includes(event.key)) {
    event.preventDefault();
    next();
  } else if (["ArrowLeft", "ArrowUp", "PageUp", "Backspace"].includes(event.key)) {
    event.preventDefault();
    previous();
  } else if (event.key === "Home") {
    event.preventDefault();
    goTo(0);
  } else if (event.key === "End") {
    event.preventDefault();
    goTo(slides.length - 1);
  } else if (event.key.toLowerCase() === "f") {
    event.preventDefault();
    toggleFullscreen();
  }
});

window.addEventListener("hashchange", () => {
  currentIndex = getInitialIndex();
  render();
});

document.addEventListener(
  "touchstart",
  (event) => {
    touchStartX = event.changedTouches[0]?.clientX ?? null;
  },
  { passive: true },
);

document.addEventListener(
  "touchend",
  (event) => {
    if (touchStartX === null) return;
    const touchEndX = event.changedTouches[0]?.clientX ?? touchStartX;
    const distance = touchEndX - touchStartX;
    touchStartX = null;

    if (Math.abs(distance) < 50) return;
    if (distance < 0) next();
    else previous();
  },
  { passive: true },
);

render();
