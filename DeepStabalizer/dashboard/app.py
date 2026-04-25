from __future__ import annotations

import itertools
import os
import sys
import threading
import time
from collections import deque

import numpy as np
from flask import Flask, jsonify, render_template

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from dashboard.demo_data import compute_demo_metrics, generate_demo_signal

app = Flask(__name__, template_folder="templates", static_folder="static")

signal_buffer: deque[list[float]] = deque(maxlen=40)
intent_buffer: deque[list[float]] = deque(maxlen=40)
safe_command_buffer: deque[list[float]] = deque(maxlen=40)
metrics_buffer: deque[dict[str, float]] = deque(maxlen=40)


def signal_stream() -> None:
    phases = itertools.count()
    while True:
        phase = next(phases) * 0.12
        _, raw_motion, intent_prediction, safe_robot_command = generate_demo_signal(duration=1, fs=100, phase=phase)
        metrics = compute_demo_metrics(raw_motion, intent_prediction, safe_robot_command)

        signal_buffer.append(raw_motion.tolist())
        intent_buffer.append(intent_prediction.tolist())
        safe_command_buffer.append(safe_robot_command.tolist())
        metrics_buffer.append(metrics)
        time.sleep(0.1)


threading.Thread(target=signal_stream, daemon=True).start()


@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/api/signal")
def get_signal():
    if not signal_buffer:
        return jsonify(
            {
                "raw": [],
                "intent_prediction": [],
                "safe_robot_command": [],
                "tremor_level": 0.0,
                "intent_score": 0.0,
                "safe_command_label": "stable motion",
                "snr_raw": 0.0,
                "snr_safe": 0.0,
                "risk_score": 0,
                "mode": "demo",
            }
        )

    raw = np.array(signal_buffer[-1], dtype=np.float32)
    intent_prediction = np.array(intent_buffer[-1], dtype=np.float32)
    safe_robot_command = np.array(safe_command_buffer[-1], dtype=np.float32)
    metrics = metrics_buffer[-1]

    return jsonify(
        {
            "raw": raw.tolist(),
            "intent_prediction": intent_prediction.tolist(),
            "safe_robot_command": safe_robot_command.tolist(),
            "intent_score": metrics["intent_score"],
            "tremor_level": metrics["tremor_level"],
            "snr_raw": metrics["snr_raw"],
            "snr_safe": metrics["snr_safe"],
            "risk_score": metrics["risk_score"],
            "safe_command_label": metrics["command_label"],
            "mode": "synthetic demo",
        }
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
