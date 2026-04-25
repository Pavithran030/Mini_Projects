from __future__ import annotations

import numpy as np
from scipy.signal import butter, filtfilt


def bandpass_filter(
    signal: np.ndarray,
    lowcut: float = 0.5,
    highcut: float = 20.0,
    fs: int = 100,
    order: int = 4,
) -> np.ndarray:
    """Apply a Butterworth bandpass filter to a 1D signal."""
    if signal.ndim != 1:
        raise ValueError("signal must be 1D")

    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="band")
    return filtfilt(b, a, signal)
