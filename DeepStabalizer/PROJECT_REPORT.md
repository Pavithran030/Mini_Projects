# DeepStable — Project Report

## 1. Summary

DeepStable is a prototype system for motion-stability monitoring. It trains a small neural network on 9-axis sensor readings (accelerometer, gyroscope, magnetometer) and classifies each reading as `stable` (0) or `unstable` (1). The project includes a web dashboard that replays dataset rows or synthetic sensor streams and shows live predictions, risk scores, and simple safety commands.

## 2. Problem Statement

Devices that move (robot arms, medical instruments, handheld devices) sometimes experience instability or tremor. Detecting unstable motion quickly allows automated systems to react (stop, slow down, or alert an operator). This project addresses the binary classification problem:

- Input: nine sensor readings: `aX, aY, aZ, gX, gY, gZ, mX, mY, mZ`.
- Output: probability of instability and a categorical label (`stable` / `unstable`).

The goal is to provide a low-latency predictor and a simple visualization/experiment environment to inspect model behavior on recorded data.

## 3. Dataset

- Location: `data/raw/Dataset.csv`
- Samples: 27,995 rows (as used in the workspace at time of writing)
- Features: `aX, aY, aZ, gX, gY, gZ, mX, mY, mZ`
- Target column: `Result` (0 stable, 1 unstable)
- Typical split in project: train ≈ 19,595, val ≈ 4,200, test ≈ 4,200

## 4. Project Structure

- `training/` — training scripts and dataset utilities
  - `train.py` — training pipeline, checkpoint saving
  - `dataset.py` — load and split dataset
  - `evaluate.py` — evaluation utilities
- `model/` — model definitions and saved artifacts
  - `sensor_classifier.py` — PyTorch model class
  - `sensor_classifier.pth` — saved checkpoint (created after training)
  - `scaler.pkl` — saved StandardScaler (created after training)
- `preprocessing/normalise.py` — normalizer wrapper
- `dashboard/` — Flask web app and static UI
  - `app.py` — server, replay loop, API endpoints
  - `templates/dashboard.html` — UI skeleton
  - `static/dashboard.js`, `style.css` — client logic and styling
- `inference.py` — thin wrapper around model + scaler for programmatic predictions
- Top-level helpers: `evaluate.py`, `README.md`, `requirements.txt`

## 5. Model and Training Details

- Architecture: small MLP (about 17k parameters)
  - Input dim: 9
  - Dense layers with BatchNorm, GELU activations, Dropout
  - Output: `num_classes=2`
- Loss: Cross-entropy with optional class weighting
- Optimizer: `AdamW`
- Learning rate scheduler: `ReduceLROnPlateau`
- Early stopping: monitored by validation loss (patience configurable)
- Feature scaling: StandardScaler fitted on training set, saved to `model/scaler.pkl`

### Checkpoint format
Training saves the best checkpoint to `model/sensor_classifier.pth` using `torch.save()` with a dictionary containing at least:

- `epoch` — saved epoch index
- `model_state` — `state_dict()` of the model weights
- `val_loss`, `val_acc` — validation metrics at save time
- `input_dim`, `num_classes` — model shape info
- `dropout` — training dropout parameter

This format allows recreating the `SensorClassifier` and loading weights for inference.

## 6. Inference API and Utilities

- `inference.DeepStablePredictor`:
  - Loads `model/sensor_classifier.pth` and `model/scaler.pkl`.
  - Methods: `predict_single(...)` and `predict_batch(ndarray)`.
  - Output (per sample): `{"class": int, "label": str, "risk_score": float, "probabilities": [p0, p1]}`

- Dashboard endpoint: `POST /api/predict` accepts JSON with the nine fields and returns the same JSON result.

- Example programmatic inference:

```python
from inference import DeepStablePredictor
p = DeepStablePredictor()
res = p.predict_single(
    aX=0.05, aY=-0.03, aZ=9.81,
    gX=0.01, gY=0.02, gZ=-0.01,
    mX=28.0, mY=-10.0, mZ=4.5,
)
print(res)
```

- Example curl call to dashboard (when running):

```bash
curl -X POST http://127.0.0.1:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"aX":0.05,"aY":-0.03,"aZ":9.81,"gX":0.01,"gY":0.02,"gZ":-0.01,"mX":28.0,"mY":-10.0,"mZ":4.5}'
```

## 7. Dashboard Behavior

- Background replay thread (`_demo_loop`) runs every 0.5s and updates an in-memory `_state` object.
- Data sources:
  - If `data/raw/Dataset.csv` exists → replay rows in sequence (this is the current behavior)
  - Otherwise → generate synthetic sensor readings
- If `model/sensor_classifier.pth` exists and can be loaded, the dashboard uses the model to produce `risk_score` and `label`. Otherwise it displays source labels or demo values.
- UI shows: risk score, motion label, tremor level, robot command (`ALLOW`, `CAUTION`, `HOLD`), charts for sensor and risk history, and last 60 history points.

## 8. What you get from the project (deliverables)

- `model/sensor_classifier.pth` — trained weights and metadata
- `model/scaler.pkl` — feature normalizer
- Live dashboard UI — replay and visualization of model output
- Programmatic inference via `inference.DeepStablePredictor` and `/api/predict`
- Training logs and optional `training_history.json`

## 9. How outputs are useful (short)

- `risk_score` can drive safety actions (HOLD/CAUTION/ALLOW)
- Probabilities allow uncertainty-aware decisions and logging of borderline cases for retraining
- Dashboard facilitates debugging and model validation on known dataset rows
- Saved artifacts are portable for deployment elsewhere or on-device inference (after conversion)

## 10. Limitations & Assumptions

- The dashboard replays the **same dataset used for training** by default; it does not support user CSV uploads out of the box.
- The model assumes the same sensor calibration and units as the training data. Inputs should be normalized the same way.
- The project is a prototype and does not include production concerns: authentication, input validation for untrusted uploads, robust logging, or secure model storage.

## 11. Next steps (suggested)

- Add CSV upload to dashboard to replay user-supplied datasets.
- Add a CLI batch-prediction tool that reads a CSV, runs `predict_batch`, and writes `predictions.csv`.
- Add logging of all live predictions for auditing and retraining (store uncertain cases).
- Optionally convert model to ONNX or TorchScript for faster serving or on-device inference.

## 12. How to run (quick commands)

Start training (from repository root):

```bash
cd training
python train.py --data "..\\data\\raw\\Dataset.csv" --model_dir "..\\model"
```

Run dashboard:

```bash
python dashboard/app.py
# Open http://127.0.0.1:5000
```

Run a single programmatic prediction:

```bash
python -c "from inference import DeepStablePredictor; print(DeepStablePredictor().predict_single(aX=0.05,aY=-0.03,aZ=9.81,gX=0.01,gY=0.02,gZ=-0.01,mX=28.0,mY=-10.0,mZ=4.5))"
```

## 13. System Architecture

The project follows a modular architecture with clear separation between training, inference, and presentation:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DeepStable System                           │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ DATA LAYER                                                           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  data/raw/Dataset.csv (27,995 samples, 9 features + label)          │
│  │                                                                  │
│  └─→ training/dataset.py (load, split: train/val/test)             │
│      └─→ preprocessing/normalise.py (StandardScaler fit)           │
│          └─→ model/scaler.pkl (saved for inference)                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ TRAINING LAYER                                                       │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  training/train.py                                                   │
│  ├─ Load & normalize data                                           │
│  ├─ Instantiate SensorClassifier (17.7k params)                     │
│  ├─ Training loop: 50 epochs, early stopping                        │
│  │  ├─ Forward pass → Cross-entropy loss                           │
│  │  ├─ Backward pass → AdamW optimizer                             │
│  │  ├─ LR scheduler: ReduceLROnPlateau                             │
│  │  └─ Validation check every epoch                                │
│  └─→ Save best checkpoint to model/sensor_classifier.pth           │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ INFERENCE LAYER                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  inference.py (DeepStablePredictor)                                 │
│  │                                                                  │
│  ├─ Load model/sensor_classifier.pth (weights + metadata)           │
│  ├─ Load model/scaler.pkl (normalizer)                             │
│  │                                                                  │
│  ├─ predict_single(aX,aY,aZ,gX,gY,gZ,mX,mY,mZ)                    │
│  │  ├─ Normalize input using fitted scaler                        │
│  │  ├─ Forward pass through model                                 │
│  │  └─ Return {class, label, risk_score, probabilities}           │
│  │                                                                  │
│  └─ predict_batch(ndarray) → list of predictions                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│ DASHBOARD LAYER                                                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  Frontend (browser)                                                  │
│  ├─ dashboard.html (UI structure)                                  │
│  ├─ dashboard.js (fetch /api/state every 1s, update UI)            │
│  └─ style.css (light theme, responsive layout)                     │
│                    ↑                                                │
│                    │ AJAX polling (every 1 second)                 │
│                    ↓                                                │
│  Backend (Flask)                                                    │
│  ├─ app.py (_demo_loop thread)                                     │
│  │  ├─ Load dataset or generate synthetic data                     │
│  │  ├─ Pass data to inference.DeepStablePredictor                 │
│  │  └─ Update _state with predictions                             │
│  │                                                                  │
│  ├─ GET  /           → Serve dashboard.html                        │
│  ├─ GET  /api/state  → Return current _state (JSON)               │
│  └─ POST /api/predict → Manual prediction endpoint                │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 14. MLP Model Architecture

The SensorClassifier is a small but effective multi-layer perceptron:

```
┌────────────────────────────────────────────────────────────────────┐
│ INPUT LAYER                                                        │
│  9 sensor values: [aX, aY, aZ, gX, gY, gZ, mX, mY, mZ]           │
│  (raw, not normalized)                                            │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────────────────────────────┐
│ NORMALIZATION (Pre-processing)                                     │
│  StandardScaler.transform(input)                                  │
│  (apply mean/std fitted on training data)                         │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────────────────────────────┐
│ HIDDEN BLOCK 1                                                     │
│  ├─ BatchNorm1d(9)           → normalize activations              │
│  ├─ Linear(9 → 64)           → 9 × 64 = 576 weights              │
│  ├─ GELU activation          → smooth non-linearity               │
│  └─ Dropout(0.3)             → 30% neurons dropped during train   │
│  Output shape: [batch_size, 64]                                   │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────────────────────────────┐
│ HIDDEN BLOCK 2                                                     │
│  ├─ BatchNorm1d(64)          → normalize activations              │
│  ├─ Linear(64 → 128)         → 64 × 128 = 8,192 weights          │
│  ├─ GELU activation          → smooth non-linearity               │
│  └─ Dropout(0.3)             → 30% neurons dropped                │
│  Output shape: [batch_size, 128]                                  │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────────────────────────────┐
│ HIDDEN BLOCK 3                                                     │
│  ├─ BatchNorm1d(128)         → normalize activations              │
│  ├─ Linear(128 → 64)         → 128 × 64 = 8,192 weights          │
│  ├─ GELU activation          → smooth non-linearity               │
│  └─ Dropout(0.2)             → 20% neurons dropped                │
│  Output shape: [batch_size, 64]                                   │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────────────────────────────┐
│ OUTPUT LAYER                                                       │
│  Linear(64 → 2)              → 64 × 2 = 128 weights               │
│  Output shape: [batch_size, 2]                                    │
│  (raw logits for 2 classes: stable, unstable)                     │
└────────────┬─────────────────────────────────────────────────────┘
             │
             ↓
┌────────────────────────────────────────────────────────────────────┐
│ SOFTMAX (Post-processing)                                          │
│  Convert logits → probabilities [P(stable), P(unstable)]          │
│  risk_score = P(unstable) = probabilities[1]                      │
└────────────────────────────────────────────────────────────────────┘

TOTAL PARAMETERS: 17,748 trainable weights
  - 576 (L1) + 8,192 (L2) + 8,192 (L3) + 128 (out) + biases
COMPUTATIONAL COST: ~40 KB model size, <1ms inference per sample
```

---

## 15. Training Pipeline Flow

Step-by-step workflow from data to trained checkpoint:

```
START: python training/train.py
  │
  ├─ Parse arguments
  │  ├─ data_path: r"D:\\files\\data\\raw\\Dataset.csv"
  │  ├─ model_dir: r"D:\\files\\model"
  │  ├─ batch_size: 128
  │  ├─ epochs: 50
  │  ├─ learning_rate: 3e-4
  │  └─ early_stop_patience: 10
  │
  ├─ Load dataset (27,995 samples)
  │  └─ Features: [aX, aY, aZ, gX, gY, gZ, mX, mY, mZ]
  │  └─ Target: [0 stable, 1 unstable]
  │  └─ Output: X (27995, 9), y (27995,)
  │
  ├─ Split dataset (train/val/test)
  │  ├─ Train: 19,595 samples (70%)
  │  ├─ Val:   4,200 samples  (15%)
  │  └─ Test:  4,200 samples  (15%)
  │
  ├─ Fit normalizer on training data
  │  ├─ Compute mean and std for each of 9 features
  │  ├─ Save to model/scaler.pkl
  │  └─ Normalize X_train, X_val, X_test
  │
  ├─ Compute class weights (for imbalanced data)
  │  ├─ stable (0): 12,749 samples → weight ≈ 1.20
  │  └─ unstable (1): 15,246 samples → weight ≈ 1.00
  │
  ├─ Initialize model SensorClassifier(9, 2)
  │  └─ 17,748 trainable parameters
  │
  ├─ Setup training components
  │  ├─ Loss: CrossEntropyLoss(weight=class_weights)
  │  ├─ Optimizer: AdamW(lr=3e-4, weight_decay=1e-5)
  │  └─ Scheduler: ReduceLROnPlateau(patience=5, factor=0.5)
  │
  ├─ FOR epoch in range(50):
  │  │
  │  ├─ TRAINING PHASE
  │  │  ├─ Set model.train()
  │  │  ├─ FOR each batch in train_loader (128 samples):
  │  │  │  ├─ Forward pass: logits = model(X_batch)
  │  │  │  ├─ Compute loss = criterion(logits, y_batch)
  │  │  │  ├─ Backward pass: loss.backward()
  │  │  │  ├─ Update weights: optimizer.step()
  │  │  │  └─ Clear gradients: optimizer.zero_grad()
  │  │  └─ Aggregate: tr_loss, tr_acc over all batches
  │  │
  │  ├─ VALIDATION PHASE
  │  │  ├─ Set model.eval()
  │  │  ├─ FOR each batch in val_loader (no gradient tracking):
  │  │  │  ├─ Forward pass: logits = model(X_batch)
  │  │  │  ├─ Compute loss = criterion(logits, y_batch)
  │  │  │  └─ Track accuracy
  │  │  └─ Aggregate: va_loss, va_acc
  │  │
  │  ├─ Scheduler step: scheduler.step(va_loss)
  │  │  └─ Reduce LR if va_loss plateaus
  │  │
  │  ├─ CHECK: If va_loss < best_val
  │  │  ├─ Update best_val = va_loss
  │  │  ├─ Save checkpoint to model/sensor_classifier.pth
  │  │  │  └─ Includes: epoch, model_state, val_loss, val_acc, input_dim, num_classes
  │  │  └─ Reset early_stop_counter = 0
  │  │
  │  ├─ ELSE: early_stop_counter += 1
  │  │  └─ If early_stop_counter >= patience(10):
  │  │     └─ BREAK (training stopped early)
  │  │
  │  └─ Log: epoch, tr_loss, va_loss, tr_acc, va_acc, lr, elapsed_time
  │
  ├─ Load best checkpoint
  │  └─ model.load_state_dict(ckpt["model_state"])
  │
  ├─ EVALUATION PHASE (on test set)
  │  ├─ Set model.eval()
  │  ├─ FOR each batch in test_loader:
  │  │  └─ Compute test loss and accuracy
  │  └─ Report final test metrics
  │
  ├─ Save training history to model/training_history.json
  │  ├─ train_loss, val_loss (per epoch)
  │  ├─ train_acc, val_acc (per epoch)
  │  └─ Useful for plotting loss curves
  │
  └─ END: Training complete
     └─ Ready for inference via inference.DeepStablePredictor()

═════════════════════════════════════════════════════════════════════
ARTIFACTS CREATED:
  ✓ model/sensor_classifier.pth     (trained weights + metadata)
  ✓ model/scaler.pkl                (feature normalizer)
  ✓ model/training_history.json     (optional: metrics per epoch)
═════════════════════════════════════════════════════════════════════
```

---

## 16. Contact / Author

Project assembled in the current workspace. For further changes, request features such as CSV upload, batch prediction script, or model conversion.

---

*Report generated automatically with system architecture, model architecture, and training pipeline diagrams.*
