from __future__ import annotations

import math

import numpy as np


def generate_demo_signal(duration: int = 1, fs: int = 100, phase: float = 0.0) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Generate synthetic raw motion, intent prediction, tremor level, and safe robot command."""
    t = np.linspace(0, duration, duration * fs, endpoint=False)

    intent_prediction = 0.45 * np.sin(2 * math.pi * 1.25 * t + phase) + 0.12 * np.sin(2 * math.pi * 0.6 * t)
    tremor_component = 0.16 * np.sin(2 * math.pi * 5.4 * t + 1.5 * phase)
    noise = 0.02 * np.random.default_rng(int(phase * 1000) % 10000).normal(size=len(t))
    raw_motion = intent_prediction + tremor_component + noise

    # Safe robot command approximates the intended motion with a reduced tremor component.
    safe_robot_command = intent_prediction + 0.03 * np.sin(2 * math.pi * 5.4 * t + 0.3 * phase)

    return (
        t.astype(np.float32),
        raw_motion.astype(np.float32),
        intent_prediction.astype(np.float32),
        safe_robot_command.astype(np.float32),
    )


def compute_demo_metrics(raw_motion: np.ndarray, intent_prediction: np.ndarray, safe_robot_command: np.ndarray) -> dict[str, float]:
    signal_power = float(np.mean(intent_prediction**2) + 1e-12)
    raw_error = float(np.mean((raw_motion - intent_prediction) ** 2) + 1e-12)
    safe_error = float(np.mean((safe_robot_command - intent_prediction) ** 2) + 1e-12)

    tremor_level = float(np.clip(np.std(raw_motion - intent_prediction) * 100.0, 0, 100))
    risk_score = int(np.clip(np.mean(np.abs(raw_motion - safe_robot_command)) * 120.0, 0, 100))
    intent_score = float(np.clip(100.0 - tremor_level, 0, 100))
    command_label = "stable motion" if risk_score < 35 else "caution hold"

    snr_raw = 10.0 * np.log10(signal_power / raw_error)
    snr_safe = 10.0 * np.log10(signal_power / safe_error)

    return {
        "intent_score": round(intent_score, 2),
        "tremor_level": round(tremor_level, 2),
        "snr_raw": round(float(snr_raw), 2),
        "snr_safe": round(float(snr_safe), 2),
        "risk_score": risk_score,
        "command_label": command_label,
    }