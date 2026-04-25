from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv

import numpy as np

FEATURE_COLUMNS = ("aX", "aY", "aZ", "gX", "gY", "gZ", "mX", "mY", "mZ")
LABEL_COLUMN = "Result"


@dataclass(frozen=True)
class Standardizer:
    mean: np.ndarray
    std: np.ndarray


def resolve_dataset_path(preferred_path: str | Path | None = None) -> Path:
    candidates: list[Path] = []

    if preferred_path is not None:
        candidates.append(Path(preferred_path))

    candidates.append(Path(__file__).resolve().parents[1] / "data" / "raw" / "Dataset.csv")
    candidates.append(Path(r"d:/Downloads/tremor/Dataset.csv"))

    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Could not find Dataset.csv. Place it in data/raw/Dataset.csv or pass --data-path."
    )


def load_sensor_csv(csv_path: str | Path) -> tuple[np.ndarray, np.ndarray, list[str]]:
    csv_path = Path(csv_path)
    rows: list[list[float]] = []
    labels: list[float] = []

    with csv_path.open("r", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            rows.append([float(row[column]) for column in FEATURE_COLUMNS])
            labels.append(float(row[LABEL_COLUMN]))

    features = np.asarray(rows, dtype=np.float32)
    targets = np.asarray(labels, dtype=np.float32)
    return features, targets, list(FEATURE_COLUMNS)


def clean_dataset(features: np.ndarray, targets: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    mask = np.isfinite(features).all(axis=1) & np.isfinite(targets)
    cleaned_features = features[mask]
    cleaned_targets = targets[mask]
    return cleaned_features.astype(np.float32), cleaned_targets.astype(np.float32)


def stratified_split(
    features: np.ndarray,
    targets: np.ndarray,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    seed: int = 42,
) -> tuple[tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray], tuple[np.ndarray, np.ndarray]]:
    if not np.isclose(train_ratio + val_ratio + test_ratio, 1.0):
        raise ValueError("split ratios must add up to 1.0")

    rng = np.random.default_rng(seed)
    train_indices: list[int] = []
    val_indices: list[int] = []
    test_indices: list[int] = []

    for label in np.unique(targets):
        class_indices = np.where(targets == label)[0]
        rng.shuffle(class_indices)

        total = len(class_indices)
        train_end = int(total * train_ratio)
        val_end = train_end + int(total * val_ratio)

        train_indices.extend(class_indices[:train_end].tolist())
        val_indices.extend(class_indices[train_end:val_end].tolist())
        test_indices.extend(class_indices[val_end:].tolist())

    rng.shuffle(train_indices)
    rng.shuffle(val_indices)
    rng.shuffle(test_indices)

    train_x, train_y = features[train_indices], targets[train_indices]
    val_x, val_y = features[val_indices], targets[val_indices]
    test_x, test_y = features[test_indices], targets[test_indices]
    return (train_x, train_y), (val_x, val_y), (test_x, test_y)


def fit_standardizer(features: np.ndarray) -> Standardizer:
    mean = features.mean(axis=0)
    std = features.std(axis=0)
    std = np.where(std == 0, 1.0, std)
    return Standardizer(mean=mean.astype(np.float32), std=std.astype(np.float32))


def apply_standardizer(features: np.ndarray, standardizer: Standardizer) -> np.ndarray:
    return ((features - standardizer.mean) / standardizer.std).astype(np.float32)


def summarize_dataset(targets: np.ndarray) -> dict[str, int]:
    unique, counts = np.unique(targets.astype(int), return_counts=True)
    return {str(label): int(count) for label, count in zip(unique, counts)}
