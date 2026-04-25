from __future__ import annotations

import numpy as np


def extract_fft_features(window: np.ndarray, fs: int = 100) -> np.ndarray:
    """Return FFT magnitudes in tremor band (3 to 12 Hz)."""
    if window.ndim != 1:
        raise ValueError("window must be 1D")

    fft_vals = np.abs(np.fft.rfft(window))
    fft_freq = np.fft.rfftfreq(len(window), d=1.0 / fs)
    mask = (fft_freq >= 3.0) & (fft_freq <= 12.0)
    return fft_vals[mask]
