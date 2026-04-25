from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from model.sensor_classifier import SensorClassifier
from training.dataset import Standardizer, apply_standardizer, clean_dataset, load_sensor_csv, resolve_dataset_path, stratified_split


DEFAULT_DATA_PATH = Path(r"d:/Downloads/tremor/Dataset.csv")
DEFAULT_CHECKPOINT = Path(__file__).resolve().parents[1] / "model" / "sensor_classifier.pth"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Evaluate the DeepStable tremor classifier.")
    parser.add_argument("--data-path", type=Path, default=None)
    parser.add_argument("--checkpoint", type=Path, default=DEFAULT_CHECKPOINT)
    return parser.parse_args()


def compute_metrics(targets: np.ndarray, probabilities: np.ndarray, threshold: float = 0.5) -> dict[str, float]:
    predictions = (probabilities >= threshold).astype(int)
    targets = targets.astype(int)

    tp = int(np.sum((predictions == 1) & (targets == 1)))
    tn = int(np.sum((predictions == 0) & (targets == 0)))
    fp = int(np.sum((predictions == 1) & (targets == 0)))
    fn = int(np.sum((predictions == 0) & (targets == 1)))

    accuracy = (tp + tn) / max(1, len(targets))
    precision = tp / max(1, tp + fp)
    recall = tp / max(1, tp + fn)
    f1 = 2 * precision * recall / max(1e-12, precision + recall)
    specificity = tn / max(1, tn + fp)
    balanced_accuracy = 0.5 * (recall + specificity)

    return {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "specificity": float(specificity),
        "balanced_accuracy": float(balanced_accuracy),
        "tp": float(tp),
        "tn": float(tn),
        "fp": float(fp),
        "fn": float(fn),
    }


def main() -> None:
    args = parse_args()
    data_path = resolve_dataset_path(args.data_path)
    features, targets, _ = load_sensor_csv(data_path)
    features, targets = clean_dataset(features, targets)
    (_, _), (_, _), (test_x, test_y) = stratified_split(features, targets)

    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    standardizer = Standardizer(mean=checkpoint["standardizer_mean"], std=checkpoint["standardizer_std"])
    test_x = apply_standardizer(test_x, standardizer)

    model = SensorClassifier(input_dim=test_x.shape[1])
    model.load_state_dict(checkpoint["model_state_dict"])
    model.eval()

    with torch.no_grad():
        logits = model(torch.tensor(test_x, dtype=torch.float32))
        probabilities = torch.sigmoid(logits).numpy()

    metrics = compute_metrics(test_y, probabilities)
    print("DeepStable dataset evaluation")
    print(f"Accuracy:  {metrics['accuracy']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"Recall:    {metrics['recall']:.4f}")
    print(f"F1 score:  {metrics['f1']:.4f}")
    print(f"Specificity: {metrics['specificity']:.4f}")
    print(f"Balanced accuracy: {metrics['balanced_accuracy']:.4f}")
    print(f"Confusion matrix: TP={int(metrics['tp'])}, TN={int(metrics['tn'])}, FP={int(metrics['fp'])}, FN={int(metrics['fn'])}")


if __name__ == "__main__":
    main()
