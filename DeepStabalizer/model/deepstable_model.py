from __future__ import annotations

import torch
import torch.nn as nn

from model.lstm_decoder import LSTMDecoder
from model.transformer_encoder import TransformerEncoder


class DeepStableModel(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.encoder = TransformerEncoder(d_model=32, nhead=4, num_layers=1, dim_ff=64)
        self.decoder = LSTMDecoder(input_size=32, hidden_size=64, num_layers=1, dropout=0.1)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        encoded = self.encoder(x)
        return self.decoder(encoded)
