"""
DeepStable - Inference Utility
Load the saved checkpoint + scaler and run predictions on new sensor readings.

Typical usage
-------------
from inference import DeepStablePredictor

predictor = DeepStablePredictor()          # loads model/sensor_classifier.pth
result    = predictor.predict_single(
    aX=0.12, aY=-0.05, aZ=9.78,
    gX=0.01, gY=0.03,  gZ=-0.02,
    mX=30.1, mY=-12.4, mZ=5.6,
)
print(result)
# {'class': 0, 'label': 'stable', 'risk_score': 0.08, 'probabilities': [0.92, 0.08]}
"""

import os
import sys
import numpy as np
import torch

sys.path.insert(0, os.path.dirname(__file__))

from model.sensor_classifier  import SensorClassifier
from preprocessing.normalise   import SensorNormalizer

# Default label map – override if your dataset has different classes
DEFAULT_LABELS = {0: "stable", 1: "unstable"}


class DeepStablePredictor:
    """
    Thin inference wrapper around the trained SensorClassifier.

    Parameters
    ----------
    model_dir : str
        Directory that contains  sensor_classifier.pth  and  scaler.pkl
    label_map : dict, optional
        Maps class index → human-readable string
    """

    def __init__(
        self,
        model_dir: str = "model",
        label_map: dict | None = None,
    ):
        self.model_dir = model_dir
        self.label_map = label_map or DEFAULT_LABELS
        self.device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self._load()

    # ── Load ─────────────────────────────────────────────────────────────────

    def _load(self):
        ckpt_path   = os.path.join(self.model_dir, "sensor_classifier.pth")
        scaler_path = os.path.join(self.model_dir, "scaler.pkl")

        for path in (ckpt_path, scaler_path):
            if not os.path.exists(path):
                raise FileNotFoundError(
                    f"Required file not found: '{path}'\n"
                    "Run  python training/train.py  first."
                )

        ckpt = torch.load(ckpt_path, map_location=self.device)
        self.model = SensorClassifier(
            input_dim=ckpt["input_dim"],
            num_classes=ckpt["num_classes"],
            dropout=0.0,          # no dropout at inference
        ).to(self.device)
        self.model.load_state_dict(ckpt["model_state"])
        self.model.eval()

        self.normalizer  = SensorNormalizer.load(scaler_path)
        self.num_classes = ckpt["num_classes"]

    # ── Predict from a NumPy array ────────────────────────────────────────────

    def predict_batch(self, X: np.ndarray) -> list[dict]:
        """
        Predict on a batch of samples.

        Parameters
        ----------
        X : ndarray of shape (N, 9) – raw (unnormalised) sensor readings

        Returns
        -------
        list of dicts, one per sample:
            {'class', 'label', 'risk_score', 'probabilities'}
        """
        X_norm = self.normalizer.transform(X.astype(np.float32))
        tensor = torch.tensor(X_norm).to(self.device)

        with torch.no_grad():
            proba = self.model.predict_proba(tensor).cpu().numpy()

        results = []
        for p in proba:
            cls        = int(np.argmax(p))
            risk_score = float(p[1]) if self.num_classes == 2 else float(1 - p[0])
            results.append({
                "class":         cls,
                "label":         self.label_map.get(cls, str(cls)),
                "risk_score":    round(risk_score, 4),
                "probabilities": [round(float(v), 4) for v in p],
            })
        return results

    # ── Predict from keyword arguments ───────────────────────────────────────

    def predict_single(
        self,
        aX: float, aY: float, aZ: float,
        gX: float, gY: float, gZ: float,
        mX: float, mY: float, mZ: float,
    ) -> dict:
        """
        Convenience method for a single reading passed as keyword arguments.
        """
        row = np.array([[aX, aY, aZ, gX, gY, gZ, mX, mY, mZ]], dtype=np.float32)
        return self.predict_batch(row)[0]


# ── Quick demo ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    predictor = DeepStablePredictor()

    # Simulate a stable-ish reading
    result = predictor.predict_single(
        aX=0.05, aY=-0.03, aZ=9.81,
        gX=0.01, gY=0.02,  gZ=-0.01,
        mX=28.0, mY=-10.0, mZ=4.5,
    )
    print("Prediction:", result)
