from __future__ import annotations

import numpy as np
from sklearn.preprocessing import StandardScaler


def normalise_signal(signal: np.ndarray) -> tuple[np.ndarray, StandardScaler]:
    """Normalise to zero mean and unit variance."""
    if signal.ndim != 1:
        raise ValueError("signal must be 1D")

    scaler = StandardScaler()
    transformed = scaler.fit_transform(signal.reshape(-1, 1)).flatten()
    return transformed, scaler
