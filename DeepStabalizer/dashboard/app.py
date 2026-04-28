"""
DeepStable - Flask Dashboard
Serves the live motion-stability dashboard.

Run
---
python dashboard/app.py
Then open  http://127.0.0.1:5000
"""

import os
import sys
import threading
import time
import random

from flask import Flask, render_template, jsonify, request

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from training.dataset import FEATURE_COLS, load_dataset

# ── Try to load the real predictor; fall back to demo mode if not trained ────
try:
    from inference import DeepStablePredictor
    predictor = DeepStablePredictor(model_dir=os.path.join(
        os.path.dirname(__file__), "..", "model"
    ))
    REAL_MODEL = True
    print("[dashboard] Real model loaded.")
except Exception as e:
    predictor  = None
    REAL_MODEL = False
    print(f"[dashboard] No trained model found ({e}). Running in demo mode.")

# ── Load the original dataset for replay when it is available ────────────────
DATASET_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "raw", "Dataset.csv")
try:
    _X_replay, _y_replay = load_dataset(DATASET_PATH)
    _replay_rows = [
        {
            **{feature: float(value) for feature, value in zip(FEATURE_COLS, row)},
            "target": int(label),
        }
        for row, label in zip(_X_replay, _y_replay)
    ]
    REPLAY_DATA = True
    print(f"[dashboard] Dataset loaded for replay ({len(_replay_rows)} rows).")
except Exception as e:
    _replay_rows = []
    REPLAY_DATA = False
    print(f"[dashboard] Dataset replay unavailable ({e}). Falling back to synthetic stream.")

# ── App ───────────────────────────────────────────────────────────────────────

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
STATIC_DIR   = os.path.join(os.path.dirname(__file__), "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

# ── In-memory state shared between the demo thread and the HTTP handlers ─────
_state_lock = threading.Lock()
_state = {
    "aX": 0.0, "aY": 0.0, "aZ": 9.81,
    "gX": 0.0, "gY": 0.0, "gZ": 0.0,
    "mX": 28.0, "mY": -10.0, "mZ": 4.5,
    "risk_score":  0.05,
    "label":       "stable",
    "tremor_level": 0.05,
    "safe_command": "ALLOW",
    "real_model":   REAL_MODEL,
    "data_source":  "dataset" if REPLAY_DATA else "synthetic",
    "history": [],
}

MAX_HISTORY = 60


def _tremor_sim(t: float, intensity: float = 0.3) -> float:
    """Produces a simple sinusoidal tremor component."""
    return intensity * (
        0.5 * random.gauss(0, 1) +
        0.3 * abs(random.gauss(0, 1))
    )


def _demo_loop():
    """Background thread that advances the replay or fallback sensor stream."""
    t = 0.0
    replay_index = 0
    while True:
        if REPLAY_DATA and _replay_rows:
            sample = _replay_rows[replay_index]
            reading = {feature: round(sample[feature], 4) for feature in FEATURE_COLS}
            source_label = "unstable" if sample["target"] == 1 else "stable"
            tremor = min(1.0, abs(reading["aX"]) * 0.2 + abs(reading["gX"]) * 1.5)
            replay_index = (replay_index + 1) % len(_replay_rows)

            if REAL_MODEL and predictor:
                result = predictor.predict_single(**reading)
                risk   = result["risk_score"]
                label  = result["label"]
            else:
                risk  = float(sample["target"])
                label = source_label
        else:
            tremor = _tremor_sim(t, intensity=0.4 if (t % 30) < 10 else 0.05)
            reading = {
                "aX": round(random.gauss(0.0, 0.1) + tremor, 4),
                "aY": round(random.gauss(0.0, 0.1),           4),
                "aZ": round(9.81 + random.gauss(0, 0.05),     4),
                "gX": round(random.gauss(0.0, 0.02) + tremor * 0.3, 4),
                "gY": round(random.gauss(0.0, 0.02),           4),
                "gZ": round(random.gauss(0.0, 0.02),           4),
                "mX": round(28.0 + random.gauss(0, 0.5),       4),
                "mY": round(-10.0 + random.gauss(0, 0.5),      4),
                "mZ": round(4.5  + random.gauss(0, 0.3),       4),
            }

            if REAL_MODEL and predictor:
                result = predictor.predict_single(**reading)
                risk   = result["risk_score"]
                label  = result["label"]
            else:
                risk  = round(min(1.0, abs(tremor) * 2 + random.uniform(0, 0.1)), 3)
                label = "unstable" if risk > 0.5 else "stable"

        tremor_level = round(min(1.0, abs(tremor) * 3), 3)
        safe_cmd     = "HOLD" if risk > 0.6 else ("CAUTION" if risk > 0.3 else "ALLOW")

        with _state_lock:
            _state.update({
                **reading,
                "risk_score":   risk,
                "label":        label,
                "tremor_level": tremor_level,
                "safe_command": safe_cmd,
                "real_model":   REAL_MODEL,
                "data_source":  "dataset" if REPLAY_DATA else "synthetic",
            })
            _state["history"].append({
                "t":     round(t, 2),
                "aX":    reading["aX"],
                "risk":  risk,
                "label": label,
            })
            if len(_state["history"]) > MAX_HISTORY:
                _state["history"].pop(0)

        t += 0.5
        time.sleep(0.5)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("dashboard.html")


@app.route("/api/state")
def api_state():
    with _state_lock:
        return jsonify(dict(_state))


@app.route("/api/predict", methods=["POST"])
def api_predict():
    """Allow the dashboard to POST raw sensor values and get a live prediction."""
    if not REAL_MODEL:
        return jsonify({"error": "Model not loaded. Train first."}), 503

    data = request.get_json(force=True)
    try:
        result = predictor.predict_single(**data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    t = threading.Thread(target=_demo_loop, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=5000, debug=False)
