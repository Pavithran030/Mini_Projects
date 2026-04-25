from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path
import os
import sys

import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.sensor_classifier import SensorClassifier
from training.dataset import apply_standardizer, clean_dataset, fit_standardizer, load_sensor_csv, resolve_dataset_path, stratified_split, summarize_dataset


DEFAULT_DATA_PATH = Path(r"d:/Downloads/tremor/Dataset.csv")
DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[1] / "model"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train DeepStable on the Kaggle tremor dataset.")
    parser.add_argument("--data-path", type=Path, default=None, help="Path to Dataset.csv")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR, help="Directory for saved model")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--patience", type=int, default=5)
    return parser.parse_args()


def make_loader(features: np.ndarray, targets: np.ndarray, batch_size: int, shuffle: bool) -> DataLoader:
    x_tensor = torch.tensor(features, dtype=torch.float32)
    y_tensor = torch.tensor(targets, dtype=torch.float32)
    dataset = TensorDataset(x_tensor, y_tensor)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def run_epoch(model: nn.Module, loader: DataLoader, loss_fn: nn.Module, optimizer: torch.optim.Optimizer | None = None) -> float:
    is_training = optimizer is not None
    model.train(is_training)
    total_loss = 0.0

    for batch_x, batch_y in loader:
        if is_training:
            optimizer.zero_grad()

        logits = model(batch_x)
        loss = loss_fn(logits, batch_y)

        if is_training:
            loss.backward()
            optimizer.step()

        total_loss += float(loss.item())

    return total_loss / max(1, len(loader))


def evaluate_accuracy(model: nn.Module, loader: DataLoader) -> float:
    model.eval()
    correct = 0
    total = 0

    with torch.no_grad():
        for batch_x, batch_y in loader:
            probabilities = torch.sigmoid(model(batch_x))
            predictions = (probabilities >= 0.5).float()
            correct += int((predictions == batch_y).sum().item())
            total += int(batch_y.numel())

    return correct / max(1, total)


def main() -> None:
    args = parse_args()
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    data_path = resolve_dataset_path(args.data_path)
    features, targets, feature_names = load_sensor_csv(data_path)
    features, targets = clean_dataset(features, targets)
    print(f"Loaded dataset: {data_path}")
    print(f"Samples: {len(features)} | Features: {feature_names}")
    print(f"Label balance: {summarize_dataset(targets)}")

    (train_x, train_y), (val_x, val_y), (test_x, test_y) = stratified_split(features, targets, seed=args.seed)
    standardizer = fit_standardizer(train_x)

    train_x = apply_standardizer(train_x, standardizer)
    val_x = apply_standardizer(val_x, standardizer)
    test_x = apply_standardizer(test_x, standardizer)

    train_loader = make_loader(train_x, train_y, batch_size=args.batch_size, shuffle=True)
    val_loader = make_loader(val_x, val_y, batch_size=args.batch_size, shuffle=False)
    test_loader = make_loader(test_x, test_y, batch_size=args.batch_size, shuffle=False)

    model = SensorClassifier(input_dim=train_x.shape[1])
    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate, weight_decay=1e-4)
    positive_count = float(np.sum(train_y == 1))
    negative_count = float(np.sum(train_y == 0))
    pos_weight = torch.tensor([negative_count / max(1.0, positive_count)], dtype=torch.float32)
    loss_fn = nn.BCEWithLogitsLoss(pos_weight=pos_weight)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)

    best_val_loss = float("inf")
    best_state = None
    best_epoch = 0
    stalled_epochs = 0

    for epoch in range(1, args.epochs + 1):
        train_loss = run_epoch(model, train_loader, loss_fn, optimizer)
        val_loss = run_epoch(model, val_loader, loss_fn)
        val_accuracy = evaluate_accuracy(model, val_loader)
        scheduler.step(val_loss)
        print(f"Epoch {epoch:02d} | train loss: {train_loss:.4f} | val loss: {val_loss:.4f} | val acc: {val_accuracy:.4f}")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            best_state = deepcopy(model.state_dict())
            best_epoch = epoch
            stalled_epochs = 0
        else:
            stalled_epochs += 1

        if stalled_epochs >= args.patience:
            print(f"Early stopping triggered at epoch {epoch:02d}.")
            break

    if best_state is not None:
        model.load_state_dict(best_state)
        print(f"Restored best model from epoch {best_epoch:02d} with val loss {best_val_loss:.4f}")

    test_loss = run_epoch(model, test_loader, loss_fn)
    test_accuracy = evaluate_accuracy(model, test_loader)
    print(f"Test loss: {test_loss:.4f}")
    print(f"Test accuracy: {test_accuracy:.4f}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.output_dir / "sensor_classifier.pth"
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "feature_names": feature_names,
            "standardizer_mean": standardizer.mean,
            "standardizer_std": standardizer.std,
            "label_name": "Result",
        },
        checkpoint_path,
    )
    print(f"Saved checkpoint: {checkpoint_path}")


if __name__ == "__main__":
    main()
