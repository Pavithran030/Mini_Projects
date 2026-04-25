"""
DeepStable - Model Evaluation
Loads the saved checkpoint and test split, then prints a full metric report.

Usage
-----
python training/evaluate.py
python training/evaluate.py --model-dir model --output-dir reports
"""

import argparse
import json
import os
import sys

import numpy as np
import torch

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from model.sensor_classifier  import SensorClassifier
from preprocessing.normalise   import SensorNormalizer

try:
    from sklearn.metrics import (
        accuracy_score,
        precision_score,
        recall_score,
        f1_score,
        confusion_matrix,
        balanced_accuracy_score,
        classification_report,
    )
    SKLEARN_OK = True
except ImportError:
    SKLEARN_OK = False
    print("[evaluate] WARNING: scikit-learn not found. Install it for full metrics.")


# ─────────────────────────────────────────────────────────────────────────────
# Load helpers
# ─────────────────────────────────────────────────────────────────────────────

def load_model(model_dir: str, device: torch.device) -> SensorClassifier:
    ckpt_path = os.path.join(model_dir, "sensor_classifier.pth")
    if not os.path.exists(ckpt_path):
        raise FileNotFoundError(
            f"No checkpoint found at '{ckpt_path}'. "
            "Run  python training/train.py  first."
        )
    ckpt = torch.load(ckpt_path, map_location=device)
    model = SensorClassifier(
        input_dim=ckpt["input_dim"],
        num_classes=ckpt["num_classes"],
        dropout=ckpt.get("dropout", 0.3),
    ).to(device)
    model.load_state_dict(ckpt["model_state"])
    model.eval()
    print(f"[evaluate] Loaded checkpoint from epoch {ckpt['epoch']}  "
          f"(val_loss={ckpt['val_loss']:.4f}  val_acc={ckpt['val_acc']:.4f})")
    return model, ckpt["num_classes"]


def load_test_data(model_dir: str):
    X_path = os.path.join(model_dir, "X_test.npy")
    y_path = os.path.join(model_dir, "y_test.npy")
    if not (os.path.exists(X_path) and os.path.exists(y_path)):
        raise FileNotFoundError(
            "Test split not found. Run  python training/train.py  first."
        )
    return np.load(X_path), np.load(y_path)


# ─────────────────────────────────────────────────────────────────────────────
# Evaluate
# ─────────────────────────────────────────────────────────────────────────────

def evaluate(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"[evaluate] Device: {device}\n")

    model, num_classes = load_model(args.model_dir, device)
    X_test, y_test     = load_test_data(args.model_dir)

    # ── Inference ─────────────────────────────────────────────────────────────
    with torch.no_grad():
        logits = model(torch.tensor(X_test, dtype=torch.float32).to(device))
        proba  = torch.softmax(logits, dim=-1).cpu().numpy()
        y_pred = logits.argmax(dim=-1).cpu().numpy()

    # ── Metrics ───────────────────────────────────────────────────────────────
    report = {}
    avg    = "binary" if num_classes == 2 else "macro"

    if SKLEARN_OK:
        report["accuracy"]          = float(accuracy_score(y_test, y_pred))
        report["precision"]         = float(precision_score(y_test, y_pred, average=avg, zero_division=0))
        report["recall"]            = float(recall_score(y_test, y_pred, average=avg, zero_division=0))
        report["f1"]                = float(f1_score(y_test, y_pred, average=avg, zero_division=0))
        report["balanced_accuracy"] = float(balanced_accuracy_score(y_test, y_pred))
        cm                          = confusion_matrix(y_test, y_pred)

        # Specificity (for binary)
        if num_classes == 2:
            tn, fp, fn, tp        = cm.ravel()
            report["specificity"] = float(tn / (tn + fp + 1e-8))
        else:
            report["specificity"] = None
    else:
        # Fallback plain accuracy
        report["accuracy"] = float((y_pred == y_test).mean())

    # ── Print ─────────────────────────────────────────────────────────────────
    sep = "═" * 45
    print(sep)
    print("  DeepStable  –  Evaluation Report")
    print(sep)
    print(f"  Test samples      : {len(y_test)}")
    print(f"  Classes           : {num_classes}")
    print(f"  Accuracy          : {report['accuracy']:.4f}  ({report['accuracy']*100:.2f}%)")

    if SKLEARN_OK:
        print(f"  Precision         : {report['precision']:.4f}")
        print(f"  Recall            : {report['recall']:.4f}")
        print(f"  F1 Score          : {report['f1']:.4f}")
        print(f"  Balanced Accuracy : {report['balanced_accuracy']:.4f}")
        if report["specificity"] is not None:
            print(f"  Specificity       : {report['specificity']:.4f}")
        print()
        print("  Confusion Matrix:")
        for row in cm:
            print("   ", row)
        print()
        print("  Classification Report:")
        print(classification_report(y_test, y_pred))

    print(sep)

    # ── Save report ───────────────────────────────────────────────────────────
    os.makedirs(args.output_dir, exist_ok=True)
    report_path = os.path.join(args.output_dir, "evaluation_report.json")
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"[evaluate] Report saved → {report_path}")

    return report


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────

def parse_args():
    p = argparse.ArgumentParser(description="DeepStable – evaluate the saved model")
    p.add_argument("--model-dir",  default="model",   help="Directory with checkpoint")
    p.add_argument("--output-dir", default="reports", help="Where to save the JSON report")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    evaluate(args)
