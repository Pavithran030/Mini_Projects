from __future__ import annotations

import numpy as np


def create_windows(
    signal: np.ndarray,
    clean_signal: np.ndarray,
    window_size: int = 100,
    step: int = 10,
) -> tuple[np.ndarray, np.ndarray]:
    """Create overlapping windows for supervised sequence learning."""
    if signal.ndim != 1 or clean_signal.ndim != 1:
        raise ValueError("signal and clean_signal must be 1D")
    if len(signal) != len(clean_signal):
        raise ValueError("signal and clean_signal must have equal length")
    if len(signal) <= window_size:
        raise ValueError("signal length must be larger than window_size")

    windows = []
    targets = []
    for i in range(0, len(signal) - window_size, step):
        windows.append(signal[i : i + window_size])
        targets.append(clean_signal[i : i + window_size])

    return np.array(windows, dtype=np.float32), np.array(targets, dtype=np.float32)
