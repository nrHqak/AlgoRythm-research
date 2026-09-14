"use strict";

// Все тайминги редактируются здесь. Суммарный основной маршрут: 115 секунд.
const PRESENTATION_CONFIG = {
  scenes: [
    { id: 1, duration: 16, reveals: [] },
    { id: 2, duration: 13, reveals: [] },
    { id: 3, duration: 20, reveals: [] },
    { id: 4, duration: 19, reveals: [] },
    { id: 5, duration: 24, reveals: [{ step: 1, at: 12 }] },
    { id: 6, duration: 23, reveals: [] },
  ],
};

const scenes = Array.from(document.querySelectorAll(".scene"));
const jumpButtons = Array.from(document.querySelectorAll("[data-jump]"));
const nextBtn = document.getElementById("nextBtn");
const prevBtn = document.getElementById("prevBtn");
const modeBtn = document.getElementById("modeBtn");
const sideBtn = document.getElementById("sideBtn");
const autoBtn = document.getElementById("autoBtn");
const fullBtn = document.getElementById("fullBtn");
const stepLabel = document.getElementById("stepLabel");
const progressFill = document.getElementById("progressFill");

let sceneIndex = 0;
let revealStep = 0;
let autoplayTimer = null;
let autoplayStartedAt = 0;
let autoplayElapsed = 0;
let autoplayPaused = false;

function maxRevealForScene(index) {
  const steps = PRESENTATION_CONFIG.scenes[index].reveals.map((item) => item.step);
  return steps.length ? Math.max(...steps) : 0;
}

function allManualStates() {
  return PRESENTATION_CONFIG.scenes.reduce((total, _scene, index) => total + maxRevealForScene(index) + 1, 0);
}

function manualStatePosition() {
  let position = 0;
  for (let index = 0; index < sceneIndex; index += 1) {
    position += maxRevealForScene(index) + 1;
  }
  return position + revealStep + 1;
}

function render() {
  scenes.forEach((scene, index) => {
    const active = index === sceneIndex;
    scene.classList.toggle("is-active", active);
    scene.setAttribute("aria-hidden", String(!active));
    if (active) {
      scene.querySelectorAll(".reveal").forEach((element) => {
        const requiredStep = Number(element.dataset.reveal || 0);
        element.classList.toggle("is-visible", requiredStep <= revealStep);
      });
    }
  });

  jumpButtons.forEach((button, index) => button.classList.toggle("is-current", index === sceneIndex));
  const maxStep = maxRevealForScene(sceneIndex);
  stepLabel.textContent = `Сцена ${sceneIndex + 1} · шаг ${revealStep + 1}/${maxStep + 1}`;
  progressFill.style.width = `${(manualStatePosition() / allManualStates()) * 100}%`;
  document.title = `AlgoRythm · сцена ${sceneIndex + 1} из 6`;
}

function goNext() {
  const maxStep = maxRevealForScene(sceneIndex);
  if (revealStep < maxStep) {
    revealStep += 1;
  } else if (sceneIndex < scenes.length - 1) {
    sceneIndex += 1;
    revealStep = 0;
  }
  stopAutoplay();
  render();
}

function goPrev() {
  if (revealStep > 0) {
    revealStep -= 1;
  } else if (sceneIndex > 0) {
    sceneIndex -= 1;
    revealStep = maxRevealForScene(sceneIndex);
  }
  stopAutoplay();
  render();
}

function goHome() {
  sceneIndex = 0;
  revealStep = 0;
  stopAutoplay();
  render();
}

function jumpTo(index) {
  sceneIndex = Math.max(0, Math.min(index, scenes.length - 1));
  revealStep = 0;
  stopAutoplay();
  render();
}

async function toggleFullscreen() {
  try {
    if (!document.fullscreenElement) {
      await document.documentElement.requestFullscreen();
    } else {
      await document.exitFullscreen();
    }
  } catch (_error) {
    // Браузер может запретить fullscreen вне пользовательского жеста.
  }
}

function toggleMode() {
  const overlay = document.body.classList.toggle("mode-overlay");
  document.body.classList.toggle("mode-monitor", !overlay);
  modeBtn.textContent = overlay ? "OVERLAY" : "MONITOR";
}

function toggleSide() {
  const visualOnLeft = document.body.classList.contains("visual-left");
  document.body.classList.toggle("visual-left", !visualOnLeft);
  document.body.classList.toggle("visual-right", visualOnLeft);
  sideBtn.textContent = visualOnLeft ? "Визуал справа" : "Визуал слева";
}

function stopAutoplay() {
  window.clearInterval(autoplayTimer);
  autoplayTimer = null;
  autoplayPaused = false;
  autoplayElapsed = 0;
  autoBtn.textContent = "▶ Авто";
}

function autoplayTick() {
  if (autoplayPaused) return;

  const sceneConfig = PRESENTATION_CONFIG.scenes[sceneIndex];
  const elapsed = autoplayElapsed + (performance.now() - autoplayStartedAt) / 1000;
  const dueReveal = sceneConfig.reveals
    .filter((item) => item.at <= elapsed)
    .reduce((max, item) => Math.max(max, item.step), 0);

  if (dueReveal > revealStep) {
    revealStep = dueReveal;
    render();
  }

  if (elapsed >= sceneConfig.duration) {
    if (sceneIndex >= scenes.length - 1) {
      stopAutoplay();
      return;
    }
    sceneIndex += 1;
    revealStep = 0;
    autoplayElapsed = 0;
    autoplayStartedAt = performance.now();
    render();
  }
}

function toggleAutoplay() {
  if (!autoplayTimer) {
    autoplayStartedAt = performance.now();
    autoplayElapsed = 0;
    autoplayPaused = false;
    autoplayTimer = window.setInterval(autoplayTick, 100);
    autoBtn.textContent = "Ⅱ Пауза";
    return;
  }

  if (!autoplayPaused) {
    autoplayElapsed += (performance.now() - autoplayStartedAt) / 1000;
    autoplayPaused = true;
    autoBtn.textContent = "▶ Продолжить";
  } else {
    autoplayStartedAt = performance.now();
    autoplayPaused = false;
    autoBtn.textContent = "Ⅱ Пауза";
  }
}

nextBtn.addEventListener("click", goNext);
prevBtn.addEventListener("click", goPrev);
modeBtn.addEventListener("click", toggleMode);
sideBtn.addEventListener("click", toggleSide);
autoBtn.addEventListener("click", toggleAutoplay);
fullBtn.addEventListener("click", toggleFullscreen);
jumpButtons.forEach((button) => button.addEventListener("click", () => jumpTo(Number(button.dataset.jump))));

document.addEventListener("keydown", (event) => {
  const tagName = event.target?.tagName?.toLowerCase();
  if (tagName === "input" || tagName === "textarea" || tagName === "select") return;

  if (event.code === "Space" || event.key === "ArrowRight") {
    event.preventDefault();
    goNext();
  } else if (event.key === "ArrowLeft") {
    event.preventDefault();
    goPrev();
  } else if (event.key === "Home") {
    event.preventDefault();
    goHome();
  } else if (event.key.toLowerCase() === "f") {
    event.preventDefault();
    toggleFullscreen();
  } else if (event.key.toLowerCase() === "h") {
    event.preventDefault();
    document.body.classList.toggle("ui-hidden");
  }
});

document.addEventListener("fullscreenchange", () => {
  fullBtn.setAttribute("aria-pressed", String(Boolean(document.fullscreenElement)));
});

render();
