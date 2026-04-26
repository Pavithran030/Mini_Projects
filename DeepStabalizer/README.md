# DeepStable – AI-Assisted Motion Stabilization Prototype

## Quick Start

```powershell
# 1  Install dependencies
pip install -r requirements.txt

# 2  Place the Kaggle tremor dataset at
#    data/raw/Dataset.csv

# 3  Train (creates model/sensor_classifier.pth and model/scaler.pkl)
python training/train.py --epochs 50

# 4  Evaluate on the held-out test set
python training/evaluate.py

# 5  Run the live dashboard
python dashboard/app.py
#    Open  http://127.0.0.1:5000
```

## Project Layout

```
deepstable/
├── data/raw/Dataset.csv          ← Kaggle tremor dataset (add manually)
├── model/
│   ├── sensor_classifier.py      ← MLP classifier definition
│   ├── sensor_classifier.pth     ← saved checkpoint (after training)
│   └── scaler.pkl                ← fitted normalizer (after training)
├── preprocessing/
│   └── normalise.py              ← SensorNormalizer (fit/transform/save/load)
├── training/
│   ├── dataset.py                ← load_dataset / split_dataset
│   ├── train.py                  ← full training loop with early stopping
│   └── evaluate.py               ← test-set metrics and confusion matrix
├── dashboard/
│   ├── app.py                    ← Flask server + demo stream
│   ├── templates/dashboard.html
│   └── static/
│       ├── dashboard.js
│       └── style.css
├── inference.py                  ← DeepStablePredictor (load & predict)
├── requirements.txt
└── README.md
```

## train.py flags

| Flag | Default | Description |
|------|---------|-------------|
| `--data` | `data/raw/Dataset.csv` | Path to input CSV |
| `--model-dir` | `model` | Where to save checkpoint + scaler |
| `--epochs` | `50` | Max training epochs |
| `--batch-size` | `128` | Mini-batch size |
| `--lr` | `3e-4` | Initial learning rate |
| `--dropout` | `0.3` | Dropout probability |
| `--patience` | `10` | Early-stopping patience |
| `--no-weighted-loss` | — | Disable class-weight balancing |
