"""
DeepStable - Feature Normalisation
Fits a StandardScaler on the training set and transforms all splits.
The fitted scaler is saved next to the model checkpoint so inference
can use exactly the same mean / std without re-fitting.
"""

import os
import pickle
import numpy as np


class SensorNormalizer:
    """
    Thin wrapper around mean / std standardisation.
    Fits only on training data, applies to all splits.
    """

    def __init__(self):
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None
        self._fitted = False

    # ── Fit ─────────────────────────────────────────────────────────────────

    def fit(self, X_train: np.ndarray) -> "SensorNormalizer":
        self.mean_ = X_train.mean(axis=0)
        self.std_  = X_train.std(axis=0)
        # Avoid division by zero for constant features
        self.std_  = np.where(self.std_ == 0, 1.0, self.std_)
        self._fitted = True
        print(f"[normalizer] Fitted on {len(X_train)} training samples")
        return self

    # ── Transform ───────────────────────────────────────────────────────────

    def transform(self, X: np.ndarray) -> np.ndarray:
        if not self._fitted:
            raise RuntimeError("SensorNormalizer.fit() must be called before transform().")
        return ((X - self.mean_) / self.std_).astype(np.float32)

    def fit_transform(self, X_train: np.ndarray) -> np.ndarray:
        return self.fit(X_train).transform(X_train)

    # ── Persistence ─────────────────────────────────────────────────────────

    def save(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump({"mean": self.mean_, "std": self.std_}, f)
        print(f"[normalizer] Scaler saved → {path}")

    @classmethod
    def load(cls, path: str) -> "SensorNormalizer":
        with open(path, "rb") as f:
            state = pickle.load(f)
        obj = cls()
        obj.mean_ = state["mean"]
        obj.std_  = state["std"]
        obj._fitted = True
        print(f"[normalizer] Scaler loaded ← {path}")
        return obj
