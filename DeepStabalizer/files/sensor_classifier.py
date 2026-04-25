"""
DeepStable - Sensor Classifier
A small but well-regularised MLP that maps 9 sensor features to a
binary (or multi-class) motion-stability label.

Architecture
------------
Input(9) → BN → Linear(64) → GELU → Dropout(0.3)
         → BN → Linear(128) → GELU → Dropout(0.3)
         → BN → Linear(64)  → GELU → Dropout(0.2)
         → Linear(num_classes)

BatchNorm before each block stabilises training on small / imbalanced sensor datasets.
"""

import torch
import torch.nn as nn


class SensorClassifier(nn.Module):
    """
    Parameters
    ----------
    input_dim   : number of sensor features (default 9)
    num_classes : number of output classes  (default 2)
    dropout     : base dropout probability  (default 0.3)
    """

    def __init__(
        self,
        input_dim:   int   = 9,
        num_classes: int   = 2,
        dropout:     float = 0.3,
    ):
        super().__init__()

        self.input_dim   = input_dim
        self.num_classes = num_classes

        self.net = nn.Sequential(
            # Block 1
            nn.BatchNorm1d(input_dim),
            nn.Linear(input_dim, 64),
            nn.GELU(),
            nn.Dropout(dropout),

            # Block 2
            nn.BatchNorm1d(64),
            nn.Linear(64, 128),
            nn.GELU(),
            nn.Dropout(dropout),

            # Block 3
            nn.BatchNorm1d(128),
            nn.Linear(128, 64),
            nn.GELU(),
            nn.Dropout(dropout * 0.67),   # slightly less aggressive last layer

            # Output
            nn.Linear(64, num_classes),
        )

        self._init_weights()

    # ── Weight initialisation ────────────────────────────────────────────────

    def _init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Linear):
                nn.init.kaiming_normal_(m.weight, nonlinearity="relu")
                if m.bias is not None:
                    nn.init.zeros_(m.bias)

    # ── Forward pass ─────────────────────────────────────────────────────────

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

    # ── Convenience: probability of the positive class ───────────────────────

    @torch.no_grad()
    def predict_proba(self, x: torch.Tensor) -> torch.Tensor:
        """Returns softmax probabilities  (B, num_classes)."""
        self.eval()
        return torch.softmax(self(x), dim=-1)

    @torch.no_grad()
    def predict(self, x: torch.Tensor) -> torch.Tensor:
        """Returns predicted class indices (B,)."""
        return self.predict_proba(x).argmax(dim=-1)


# ── Quick sanity-check ───────────────────────────────────────────────────────
if __name__ == "__main__":
    model = SensorClassifier(input_dim=9, num_classes=2)
    dummy = torch.randn(8, 9)
    print("output shape:", model(dummy).shape)   # expect (8, 2)
    print(model)
