/* DeepStable – dashboard.js */

const MAX_POINTS = 60;

// ── Chart helpers ────────────────────────────────────────────────────────────

function makeChart(id, label, color) {
  const ctx = document.getElementById(id).getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: {
      labels: [],
      datasets: [{
        label,
        data: [],
        borderColor: color,
        backgroundColor: color + "22",
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        borderWidth: 2,
      }]
    },
    options: {
      animation: false,
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { display: false },
        y: {
          ticks: { color: "#6b7a9d", font: { family: "Courier New" } },
          grid:  { color: "#1e2740" },
        }
      },
      plugins: { legend: { display: false } },
    }
  });
}

// ── Push one point, trim to MAX_POINTS ───────────────────────────────────────

function pushPoint(chart, label, value) {
  chart.data.labels.push(label);
  chart.data.datasets[0].data.push(value);
  if (chart.data.labels.length > MAX_POINTS) {
    chart.data.labels.shift();
    chart.data.datasets[0].data.shift();
  }
  chart.update("none");
}

// ── Colour helpers ───────────────────────────────────────────────────────────

function riskLevel(r) {
  if (r < 0.3)  return "low";
  if (r < 0.6)  return "medium";
  return "high";
}

function riskColor(r) {
  if (r < 0.3)  return "#22c55e";
  if (r < 0.6)  return "#f59e0b";
  return "#ef4444";
}

// ── DOM references ────────────────────────────────────────────────────────────

const $risk    = document.getElementById("risk-val");
const $riskBar = document.getElementById("risk-bar");
const $state   = document.getElementById("state-val");
const $tremor  = document.getElementById("tremor-val");
const $trBar   = document.getElementById("tremor-bar");
const $cmd     = document.getElementById("cmd-val");
const $cardRisk= document.getElementById("card-risk");
const $row     = document.getElementById("sensor-row");
const $badge   = document.getElementById("mode-badge");

// ── Init charts ───────────────────────────────────────────────────────────────

const chartAX   = makeChart("chart-ax",   "aX",        "#38bdf8");
const chartRisk = makeChart("chart-risk", "Risk Score", "#ef4444");

let tick = 0;

// ── Polling ───────────────────────────────────────────────────────────────────

async function poll() {
  try {
    const res   = await fetch("/api/state");
    const state = await res.json();

    const r   = state.risk_score   ?? 0;
    const tr  = state.tremor_level ?? 0;
    const lbl = state.label        ?? "—";
    const cmd = state.safe_command ?? "—";
    const lvl = riskLevel(r);
    const col = riskColor(r);

    // Cards
    $risk.textContent        = r.toFixed(3);
    $risk.dataset.level      = lvl;
    $riskBar.style.width     = (r * 100).toFixed(1) + "%";
    $riskBar.style.background= col;
    $cardRisk.dataset.level  = lvl;

    $state.textContent = lbl.toUpperCase();
    $state.className   = "card-value card-value--state " + lbl;

    $tremor.textContent    = tr.toFixed(3);
    $trBar.style.width     = (tr * 100).toFixed(1) + "%";

    $cmd.textContent = cmd;
    $cmd.className   = "card-value card-value--cmd " + cmd;

    // Badge
    if (state.real_model) {
      $badge.textContent  = "REAL MODEL";
      $badge.className    = "badge badge--real";
    }

    // Sensor row
    const keys = ["aX","aY","aZ","gX","gY","gZ","mX","mY","mZ"];
    $row.innerHTML = keys
      .map(k => `<td>${(state[k] ?? 0).toFixed(3)}</td>`)
      .join("");

    // Charts
    pushPoint(chartAX,   tick, state.aX ?? 0);
    pushPoint(chartRisk, tick, r);
    tick++;

  } catch (e) {
    console.warn("poll error:", e);
  }
}

// Poll every 500 ms
setInterval(poll, 500);
poll();
