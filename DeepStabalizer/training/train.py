"""
DeepStable - Training Pipeline
Trains the SensorClassifier on the Kaggle tremor dataset.

Usage
-----
python training/train.py                        # default settings
python training/train.py --epochs 30 --lr 1e-3
python training/train.py --data data/raw/Dataset.csv --batch-size 64
"""

import argparse
import os
import sys
import time
import json

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

# Allow imports from the project root regardless of CWD
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from training.dataset       import load_dataset, split_dataset
from preprocessing.normalise import SensorNormalizer
from model.sensor_classifier import SensorClassifier


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def make_loader(X, y, batch_size, shuffle):
    ds = TensorDataset(
        torch.tensor(X, dtype=torch.float32),
        torch.tensor(y, dtype=torch.long),
    )
    return DataLoader(ds, batch_size=batch_size, shuffle=shuffle, num_workers=0)


def compute_class_weights(y_train: np.ndarray, num_classes: int) -> torch.Tensor:
    """Inverse-frequency weighting to handle class imbalance."""
    counts = np.bincount(y_train, minlength=num_classes).astype(float)
    weights = 1.0 / (counts + 1e-8)
    weights /= weights.sum()
    weights *= num_classes          # scale so mean weight ≈ 1
    return torch.tensor(weights, dtype=torch.float32)


def accuracy(logits: torch.Tensor, labels: torch.Tensor) -> float:
    preds = logits.argmax(dim=-1)
    return (preds == labels).float().mean().item()


class EarlyStopper:
    def __init__(self, patience: int = 10, min_delta: float = 1e-4):
        self.patience  = patience
        self.min_delta = min_delta
        self.best_val  = float("inf")
        self.counter   = 0

    def step(self, val_loss: float) -> bool:
        """Returns True when training should stop."""
        if val_loss < self.best_val - self.min_delta:
            self.best_val = val_loss
            self.counter  = 0
            return False
        self.counter += 1
        return self.counter >= self.patience


# ─────────────────────────────────────────────────────────────────────────────
# Train
# ─────────────────────────────────────────────────────────────────────────────

def train(args):
    device = torch.device(
        "cuda" if torch.cuda.is_available() else
        "mps"  if torch.backends.mps.is_available() else
        "cpu"
    )
    print(f"[train] Device: {device}")

    # ── Load & split data ────────────────────────────────────────────────────
    X, y = load_dataset(args.data)
    X_train, X_val, X_test, y_train, y_val, y_test = split_dataset(
        X, y,
        val_ratio=args.val_ratio,
        test_ratio=args.test_ratio,
        random_state=args.seed,
    )

    # ── Normalise ────────────────────────────────────────────────────────────
    normalizer = SensorNormalizer()
    X_train = normalizer.fit_transform(X_train)
    X_val   = normalizer.transform(X_val)
    X_test  = normalizer.transform(X_test)   # kept for evaluate.py

    os.makedirs(args.model_dir, exist_ok=True)
    normalizer.save(os.path.join(args.model_dir, "scaler.pkl"))

    # Save the test split so evaluate.py can load it without re-splitting
    np.save(os.path.join(args.model_dir, "X_test.npy"), X_test)
    np.save(os.path.join(args.model_dir, "y_test.npy"), y_test)

    # ── Data loaders ─────────────────────────────────────────────────────────
    train_loader = make_loader(X_train, y_train, args.batch_size, shuffle=True)
    val_loader   = make_loader(X_val,   y_val,   args.batch_size, shuffle=False)

    # ── Model ─────────────────────────────────────────────────────────────────
    num_classes = int(y.max()) + 1
    model = SensorClassifier(
        input_dim=X_train.shape[1],
        num_classes=num_classes,
        dropout=args.dropout,
    ).to(device)

    print(f"[train] Model params: {sum(p.numel() for p in model.parameters()):,}")

    # ── Loss with class-weight support ───────────────────────────────────────
    class_weights = compute_class_weights(y_train, num_classes).to(device)
    criterion     = nn.CrossEntropyLoss(weight=class_weights if args.weighted_loss else None)

    # ── Optimiser + scheduler ─────────────────────────────────────────────────
    optimizer = torch.optim.AdamW(
        model.parameters(), lr=args.lr, weight_decay=args.weight_decay
    )
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode="min", factor=0.5, patience=5, verbose=True
    )

    stopper    = EarlyStopper(patience=args.patience)
    best_val   = float("inf")
    history    = {"train_loss": [], "val_loss": [], "train_acc": [], "val_acc": []}

    # ── Training loop ─────────────────────────────────────────────────────────
    print(f"\n{'Epoch':>6}  {'Train Loss':>11}  {'Val Loss':>10}  "
          f"{'Train Acc':>10}  {'Val Acc':>9}  {'LR':>9}  {'Time':>7}")
    print("─" * 75)

    for epoch in range(1, args.epochs + 1):
        t0 = time.time()

        # ── Train ──────────────────────────────────────────────────────────
        model.train()
        tr_loss, tr_acc = 0.0, 0.0
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            optimizer.zero_grad()
            logits = model(xb)
            loss   = criterion(logits, yb)
            loss.backward()
            nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            tr_loss += loss.item() * len(xb)
            tr_acc  += accuracy(logits, yb) * len(xb)

        tr_loss /= len(X_train)
        tr_acc  /= len(X_train)

        # ── Validate ───────────────────────────────────────────────────────
        model.eval()
        va_loss, va_acc = 0.0, 0.0
        with torch.no_grad():
            for xb, yb in val_loader:
                xb, yb = xb.to(device), yb.to(device)
                logits  = model(xb)
                va_loss += criterion(logits, yb).item() * len(xb)
                va_acc  += accuracy(logits, yb) * len(xb)

        va_loss /= len(X_val)
        va_acc  /= len(X_val)

        scheduler.step(va_loss)

        history["train_loss"].append(tr_loss)
        history["val_loss"].append(va_loss)
        history["train_acc"].append(tr_acc)
        history["val_acc"].append(va_acc)

        elapsed = time.time() - t0
        current_lr = optimizer.param_groups[0]["lr"]
        print(f"{epoch:>6}  {tr_loss:>11.4f}  {va_loss:>10.4f}  "
              f"{tr_acc:>9.4f}   {va_acc:>8.4f}  {current_lr:>9.2e}  {elapsed:>5.1f}s")

        # ── Save best checkpoint ───────────────────────────────────────────
        if va_loss < best_val:
            best_val = va_loss
            ckpt_path = os.path.join(args.model_dir, "sensor_classifier.pth")
            torch.save(
                {
                    "epoch":       epoch,
                    "model_state": model.state_dict(),
                    "val_loss":    va_loss,
                    "val_acc":     va_acc,
                    "input_dim":   X_train.shape[1],
                    "num_classes": num_classes,
                    "dropout":     args.dropout,
                },
                ckpt_path,
            )

        # ── Early stopping ─────────────────────────────────────────────────
        if stopper.step(va_loss):
            print(f"\n[train] Early stopping at epoch {epoch} (patience={args.patience})")
            break

    # ── Save training history ─────────────────────────────────────────────────
    history_path = os.path.join(args.model_dir, "training_history.json")
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    print(f"\n[train] Best val loss: {best_val:.4f}")
    print(f"[train] Checkpoint saved → {ckpt_path}")
    print(f"[train] History saved   → {history_path}")
    print("[train] Done. Run  python training/evaluate.py  to see test metrics.")


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="DeepStable – train the SensorClassifier")
    p.add_argument("--data",          default="data/raw/Dataset.csv",
                   help="Path to the Kaggle tremor CSV")
    p.add_argument("--model-dir",     default="model",
                   help="Directory to save checkpoint + scaler")
    p.add_argument("--epochs",        type=int,   default=50)
    p.add_argument("--batch-size",    type=int,   default=128)
    p.add_argument("--lr",            type=float, default=3e-4)
    p.add_argument("--weight-decay",  type=float, default=1e-4)
    p.add_argument("--dropout",       type=float, default=0.3)
    p.add_argument("--val-ratio",     type=float, default=0.15)
    p.add_argument("--test-ratio",    type=float, default=0.15)
    p.add_argument("--patience",      type=int,   default=10,
                   help="Early-stopping patience (epochs)")
    p.add_argument("--seed",          type=int,   default=42)
    p.add_argument("--no-weighted-loss", dest="weighted_loss",
                   action="store_false", default=True,
                   help="Disable inverse-frequency class weighting")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    train(args)
