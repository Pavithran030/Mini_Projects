# DeepStable 1-Hour Development Plan (Execution-First)

## Goal for this 60-minute sprint
Build a functional end-to-end prototype of DeepStable that:
- Generates tremor-like data (synthetic)
- Runs preprocessing (bandpass, normalization, windowing)
- Trains a lightweight Transformer + BiLSTM model quickly
- Serves live inference through Flask API
- Shows raw vs filtered signal and basic metrics on a web dashboard

Important scope note:
- In 1 hour, the realistic outcome is a working prototype, not full clinical-grade validation.
- Clinical metrics, real dataset integration, PDF reporting, and robust benchmarking are moved to post-sprint tasks.

---

## Architecture used from your files
Pipeline implemented in this sprint:
1. Raw signal input
2. Preprocessing: bandpass + normalization
3. Feature preparation: sliding windows (FFT optional if time remains)
4. AI core: Transformer encoder + BiLSTM decoder
5. Training with MSE + tremor penalty
6. Evaluation: RMSE, SNR improvement, tremor reduction percent
7. Flask dashboard: live raw vs filtered waveform + risk score + metrics

---

## Final deliverables at minute 60
1. Project folder structure created
2. Python dependencies installed
3. Trained model weights saved
4. Flask app running on localhost:5000
5. Dashboard visualizing live raw vs filtered signal
6. API endpoint returning metrics JSON
7. Readme notes for how to run

---

## Minute-by-minute execution plan

### 00:00 to 05:00 - Setup and scaffolding
Target outcome:
- Working folder layout and environment ready.

Tasks:
1. Create folders:
   - data/raw
   - data/processed
   - data/synthetic
   - model
   - preprocessing
   - training
   - dashboard/templates
   - dashboard/static
   - reports
2. Create starter files:
   - preprocessing/bandpass.py
   - preprocessing/normalise.py
   - preprocessing/windowing.py
   - model/transformer_encoder.py
   - model/lstm_decoder.py
   - model/deepstable_model.py
   - training/loss.py
   - training/train.py
   - training/evaluate.py
   - dashboard/app.py
   - dashboard/templates/dashboard.html
   - dashboard/static/dashboard.js
   - dashboard/static/style.css
   - requirements.txt
   - README.md

Definition of done:
- All files exist and import paths are planned.

---

### 05:00 to 10:00 - Dependencies and run check
Target outcome:
- Environment can import all required libraries.

Dependencies:
- torch
- numpy
- scipy
- scikit-learn
- flask
- matplotlib
- pandas

Tasks:
1. Install dependencies from requirements.txt
2. Run one import smoke test in Python

Definition of done:
- No import error for core packages.

---

### 10:00 to 20:00 - Data simulation and preprocessing
Target outcome:
- Synthetic supervised pairs created: raw signal and clean target.

Tasks:
1. Implement synthetic signal generator in training/train.py or preprocessing module:
   - intentional motion: 0 to 3 Hz
   - tremor: 3 to 12 Hz
   - noise: small gaussian
2. Implement preprocessing:
   - Butterworth bandpass filter (0.5 to 20 Hz)
   - standard normalization
   - sliding window creation (window size 100, step 10)
3. Save a small sample in data/synthetic for reproducibility.

Definition of done:
- Arrays prepared with shapes compatible for model training.

---

### 20:00 to 30:00 - Model implementation
Target outcome:
- Forward pass works for Transformer + BiLSTM hybrid.

Tasks:
1. Implement PositionalEncoding and TransformerEncoder
2. Implement BiLSTM decoder and final dense projection
3. Implement DeepStableModel wrapper
4. Add a simple shape test using one random batch

Recommended fast config for 1-hour sprint:
- d_model: 32
- heads: 4
- transformer layers: 1
- lstm hidden: 64
- lstm layers: 1

Definition of done:
- Model input and output shape both equal (batch, seq_len, 1).

---

### 30:00 to 40:00 - Training loop and quick model fit
Target outcome:
- Train a usable checkpoint quickly.

Tasks:
1. Implement TremorAwareLoss:
   - loss = MSE(pred, target) + weight * residual energy
2. Build DataLoader from synthetic windows
3. Train quickly for 5 to 10 epochs
4. Save checkpoint to model/deepstable_model.pth

Speed-first training choices:
- batch size: 32
- epochs: 5 (extend to 10 only if fast)
- learning rate: 1e-3
- gradient clipping: 1.0

Definition of done:
- Loss decreases and model file saved.

---

### 40:00 to 48:00 - Evaluation utilities
Target outcome:
- Metrics computed and printed for one test batch.

Tasks:
1. Implement in training/evaluate.py:
   - RMSE
   - SNR
   - tremor reduction percent
2. Evaluate raw vs filtered on held-out synthetic data
3. Print concise summary in terminal

Definition of done:
- You have metric numbers showing improvement over raw baseline.

---

### 48:00 to 57:00 - Flask backend and live API
Target outcome:
- Web server returns live inference payload.

Tasks:
1. Build Flask app in dashboard/app.py:
   - route / serves dashboard
   - route /api/signal returns JSON: raw, filtered, snr_raw, snr_filtered, risk_score
2. Start a background signal stream thread:
   - generate 1-second synthetic signal chunks
   - run model inference
   - push latest buffers
3. Add graceful fallback if model file is missing

Definition of done:
- Hitting /api/signal returns valid JSON repeatedly.

---

### 57:00 to 60:00 - Frontend wiring and demo run
Target outcome:
- Dashboard renders live before/after signal and key values.

Tasks:
1. dashboard.html:
   - chart canvas
   - metric cards
2. dashboard.js:
   - poll /api/signal every 200 ms
   - update waveform and metrics
3. style.css:
   - clean dark-light contrast and readable layout
4. Final run test:
   - start Flask
   - open browser
   - confirm updates are live

Definition of done:
- Visible real-time waveform and changing metrics in browser.

---

## Critical path (if time slips)
If behind schedule, keep these only:
1. Synthetic data + preprocessing
2. Model forward pass
3. Train 3 epochs
4. Flask endpoint returning raw and filtered arrays
5. Basic line chart with polling

Defer these to next session:
- FFT feature branch
- ROC-AUC, sensitivity, specificity
- PDF clinical report
- UCI Parkinson dataset integration
- case study write-up automation

---

## Suggested file ownership map
- preprocessing/bandpass.py: filter logic
- preprocessing/normalise.py: scaler wrapper
- preprocessing/windowing.py: segmentation
- model/transformer_encoder.py: attention stack
- model/lstm_decoder.py: sequence decoder
- model/deepstable_model.py: hybrid model composition
- training/loss.py: TremorAwareLoss
- training/train.py: data gen + train loop + save model
- training/evaluate.py: RMSE/SNR/tremor metrics
- dashboard/app.py: Flask routes + inference streaming
- dashboard/templates/dashboard.html: UI shell
- dashboard/static/dashboard.js: polling + charts
- dashboard/static/style.css: styling

---

## 1-hour acceptance checklist
Use this exact checklist before stopping:
- Project structure exists
- Dependencies installed
- Training script runs end to end
- model/deepstable_model.pth created
- Evaluation script outputs RMSE and SNR values
- Flask app starts without error
- /api/signal returns non-empty raw and filtered arrays
- Dashboard updates every less than 300 ms

---

## Immediate next 2-hour extension (after sprint)
1. Replace synthetic data with UCI Parkinson telemonitoring mapping pipeline
2. Add FFT tremor-band energy panel
3. Add sensitivity, specificity, ROC-AUC computation
4. Add experiment logging and best-model checkpointing
5. Add downloadable PDF clinical report
6. Add reproducibility: fixed seeds and config file

---

## Risk controls during the sprint
- Keep model small to avoid training delays.
- Do not chase visual perfection before API works.
- If training fails, use untrained model only to complete API and dashboard integration.
- Save checkpoints often after each working stage.

---

## One-command execution order (recommended)
1. Install dependencies
2. Run training script
3. Run evaluation script
4. Start Flask app
5. Open dashboard in browser

This sequencing gives the highest probability of a complete demo in 60 minutes.
