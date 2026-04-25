const ctx = document.getElementById('signalChart').getContext('2d');

const labels = Array.from({ length: 100 }, (_, i) => i);
const chart = new Chart(ctx, {
  type: 'line',
  data: {
    labels,
    datasets: [
      {
        label: 'Raw Signal',
        data: labels.map(() => 0),
        borderColor: '#f97316',
        borderWidth: 2,
        tension: 0.2,
        pointRadius: 0,
      },
      {
        label: 'Intent Prediction',
        data: labels.map(() => 0),
        borderColor: '#93c5fd',
        borderWidth: 2,
        borderDash: [6, 5],
        tension: 0.2,
        pointRadius: 0,
      },
      {
        label: 'Safe Robot Command',
        data: labels.map(() => 0),
        borderColor: '#10b981',
        borderWidth: 2,
        tension: 0.2,
        pointRadius: 0,
      },
    ],
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    scales: {
      x: {
        ticks: { color: '#d6d8db' },
        grid: { color: 'rgba(214, 216, 219, 0.12)' },
      },
      y: {
        ticks: { color: '#d6d8db' },
        grid: { color: 'rgba(214, 216, 219, 0.12)' },
      },
    },
    plugins: {
      legend: {
        labels: { color: '#f3f4f6' },
      },
    },
  },
});

async function updateData() {
  try {
    const res = await fetch('/api/signal');
    const payload = await res.json();

    chart.data.datasets[0].data = payload.raw || [];
    chart.data.datasets[1].data = payload.intent_prediction || [];
    chart.data.datasets[2].data = payload.safe_robot_command || [];
    chart.update();

    document.getElementById('intentPrediction').textContent = `${payload.intent_score.toFixed(2)}%`;
    document.getElementById('tremorLevel').textContent = `${payload.tremor_level.toFixed(2)}%`;
    document.getElementById('safeCommand').textContent = payload.safe_command_label || 'stable motion';
    document.getElementById('riskScore').textContent = `${payload.risk_score}`;
    document.getElementById('modeLabel').textContent = payload.mode || 'synthetic demo';
  } catch (err) {
    console.error('Failed to update signal:', err);
  }
}

setInterval(updateData, 200);
updateData();
