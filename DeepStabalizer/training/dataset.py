"""
DeepStable - Dataset Loader and Splitter
Loads the Kaggle tremor/motion sensor dataset, cleans it, and splits into
train / validation / test sets.
"""

import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

FEATURE_COLS = ["aX", "aY", "aZ", "gX", "gY", "gZ", "mX", "mY", "mZ"]
TARGET_COL   = "Result"


def load_dataset(csv_path: str) -> tuple[np.ndarray, np.ndarray]:
    """
    Load the raw CSV, drop invalid rows, and return (X, y) as NumPy arrays.

    Returns
    -------
    X : ndarray of shape (N, 9)  – sensor features
    y : ndarray of shape (N,)    – integer labels
    """
    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Dataset not found at '{csv_path}'.\n"
            "Download the Kaggle tremor dataset and place it at data/raw/Dataset.csv"
        )

    df = pd.read_csv(csv_path)

    # ── Validate expected columns ────────────────────────────────────────────
    missing = [c for c in FEATURE_COLS + [TARGET_COL] if c not in df.columns]
    if missing:
        raise ValueError(
            f"The following required columns are missing from the CSV: {missing}\n"
            f"Found columns: {list(df.columns)}"
        )

    # ── Drop rows with any NaN / Inf in feature or target columns ────────────
    before = len(df)
    df = df[FEATURE_COLS + [TARGET_COL]].copy()
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    after = len(df)

    if before != after:
        print(f"[dataset] Dropped {before - after} invalid rows  ({after} remain)")

    X = df[FEATURE_COLS].values.astype(np.float32)
    y = df[TARGET_COL].values

    # ── Encode labels to 0 / 1 if they are not already integers ─────────────
    if y.dtype == object or str(y.dtype).startswith("float"):
        classes = np.unique(y)
        label_map = {cls: idx for idx, cls in enumerate(classes)}
        y = np.array([label_map[v] for v in y], dtype=np.int64)
        print(f"[dataset] Label mapping: {label_map}")
    else:
        y = y.astype(np.int64)

    print(f"[dataset] Loaded {len(X)} samples | {len(np.unique(y))} classes | "
          f"class counts: {dict(zip(*np.unique(y, return_counts=True)))}")

    return X, y


def split_dataset(
    X: np.ndarray,
    y: np.ndarray,
    val_ratio:  float = 0.15,
    test_ratio: float = 0.15,
    random_state: int = 42,
) -> tuple:
    """
    Split (X, y) into train / val / test.

    Returns
    -------
    (X_train, X_val, X_test, y_train, y_val, y_test)
    """
    # First split off the test set
    X_temp, X_test, y_temp, y_test = train_test_split(
        X, y,
        test_size=test_ratio,
        random_state=random_state,
        stratify=y,
    )

    # Then split validation from the remainder
    relative_val = val_ratio / (1.0 - test_ratio)
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp,
        test_size=relative_val,
        random_state=random_state,
        stratify=y_temp,
    )

    print(
        f"[dataset] Split sizes → "
        f"train={len(X_train)}  val={len(X_val)}  test={len(X_test)}"
    )
    return X_train, X_val, X_test, y_train, y_val, y_test
