# DeepStable Prototype

DeepStable is a rapid prototype for physiological tremor cancellation using a Transformer + BiLSTM model.

## Quick Start

1. Create and activate venv:
   - Windows PowerShell:
     - `python -m venv venv`
     - `venv\Scripts\Activate.ps1`
2. Install deps:
   - `pip install -r requirements.txt`
3. Train a quick model:
   - `python training/train.py`
4. Evaluate:
   - `python training/evaluate.py`
5. Run dashboard:
   - `python dashboard/app.py`
6. Open http://127.0.0.1:5000

## Notes

- This implementation uses synthetic data for fast prototyping.
- Model checkpoint is saved to `model/deepstable_model.pth`.
