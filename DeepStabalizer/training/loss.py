from __future__ import annotations

import torch
import torch.nn as nn


class TremorAwareLoss(nn.Module):
    def __init__(self, tremor_penalty_weight: float = 0.3) -> None:
        super().__init__()
        self.mse = nn.MSELoss()
        self.w = tremor_penalty_weight

    def forward(self, pred: torch.Tensor, target: torch.Tensor, raw: torch.Tensor) -> torch.Tensor:
        mse_loss = self.mse(pred, target)
        residual = pred - target
        tremor_penalty = torch.mean(residual**2)
        return mse_loss + self.w * tremor_penalty
