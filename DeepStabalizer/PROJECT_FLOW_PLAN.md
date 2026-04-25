# DeepStable Project Flow Plan

## 1. Project Goal
DeepStable is an AI-based motion stabilization project for robotic surgical assistance. Its purpose is to take motion sensor data, learn the motion pattern, detect unstable movement or tremor, and produce a safer robot command or stabilized output for visualization.

The project is built as a research and demo prototype, not as a clinical surgical robot system.

---

## 2. Simple Project Idea
The project works like this:
- A person moves their hand or controller.
- The motion signal may contain tremor or instability.
- The AI model learns from the dataset.
- The model predicts whether the motion is stable or risky.
- The dashboard shows raw motion, intent prediction, tremor level, safe robot command, and risk score.

---

## 3. End-to-End Flow
This section explains the full project flow from start to finish.

### Step 1: Collect the dataset
- The shared Kaggle dataset is used as the training source.
- File: `data/raw/Dataset.csv`
- Columns:
  - `aX`, `aY`, `aZ` = accelerometer readings
  - `gX`, `gY`, `gZ` = gyroscope readings
  - `mX`, `mY`, `mZ` = motion-related values
  - `Result` = target label

### Step 2: Load and clean the data
- The CSV is loaded into the training pipeline.
- Missing or invalid values are removed.
- The sensor features are separated from the target label.

### Step 3: Split the dataset
- The data is split into:
  - training set
  - validation set
  - test set
- This helps measure how well the model works on unseen data.

### Step 4: Normalize the features
- The training set is used to calculate mean and standard deviation.
- All three splits are standardized using the same scaling values.
- This makes training more stable.

### Step 5: Train the model
- The model is a small neural classifier.
- It learns to map the 9 sensor features to the target `Result`.
- The classifier predicts whether the motion state is safe or risky.
- Training saves the learned weights to a checkpoint file.

### Step 6: Evaluate the model
- The trained model is tested on the held-out test set.
- The evaluation prints:
  - accuracy
  - precision
  - recall
  - F1 score
  - specificity
  - balanced accuracy
  - confusion matrix

### Step 7: Use the model in the dashboard
- The dashboard is powered by Flask.
- A synthetic demo stream is shown for explanation.
- The dashboard displays:
  - raw motion
  - intent prediction
  - tremor level
  - safe robot command
  - risk score

### Step 8: Show the final output
- The final output is a clear visual demo of how the system supports safer motion.
- It does not directly control a real surgical robot.
- It demonstrates how AI can support motion decision-making.

---

## 4. Working Principle
DeepStable uses the following logic:
1. Read motion sensor data.
2. Convert the data into a clean numerical format.
3. Train the AI model on the dataset.
4. Predict the motion state.
5. Convert the prediction into a safe command or risk result.
6. Display the result in the dashboard.

In simple terms:
- input = sensor motion
- processing = preprocessing + AI model
- output = safe motion decision and risk display

---

## 5. Project Modules

### 5.1 Data Module
Purpose:
- store and load the dataset

Main folder:
- `data/raw/`

### 5.2 Preprocessing Module
Purpose:
- clean data
- normalize data
- split data for training and testing

Files:
- `training/dataset.py`
- `preprocessing/bandpass.py`
- `preprocessing/normalise.py`
- `preprocessing/windowing.py`

### 5.3 Model Module
Purpose:
- classify the motion state from sensor features

Files:
- `model/sensor_classifier.py`

### 5.4 Training Module
Purpose:
- train the AI model
- save the checkpoint

Files:
- `training/train.py`

### 5.5 Evaluation Module
Purpose:
- test the model
- print performance metrics

Files:
- `training/evaluate.py`

### 5.6 Dashboard Module
Purpose:
- display the project output visually

Files:
- `dashboard/app.py`
- `dashboard/demo_data.py`
- `dashboard/templates/dashboard.html`
- `dashboard/static/dashboard.js`
- `dashboard/static/style.css`

---

## 6. Training Flow in Detail

### Input to training
- `Dataset.csv`
- sensor values and target label

### Preprocessing steps
- load CSV
- clean invalid rows
- split into train/val/test
- standardize numeric features

### Model training
- model receives 9 input features
- output is a single binary classification value
- optimizer updates weights
- validation is checked every epoch
- early stopping is used to prevent overfitting

### Saved output
- checkpoint file is saved in the model folder
- saved file:
  - `model/sensor_classifier.pth`

---

## 7. Dashboard Flow in Detail
The dashboard is kept as a demo interface so the idea is easy to understand.

### What it shows
- raw motion
- intent prediction
- tremor level
- safe robot command
- risk score

### How it works
- Flask serves the page.
- Synthetic demo data is generated.
- The chart updates live.
- Metric cards update continuously.

### Why it is useful
- makes the project easy to present
- visually explains the AI-assisted motion concept
- shows how the final system would behave in principle

---

## 8. Final Output
The final project output includes:
- a trained classifier for the Kaggle sensor dataset
- a checkpoint file for the model
- an evaluation report from the test set
- a live dashboard for explanation
- a clear flow from raw data to safe robot command

---

## 9. What the AI Model Learns
The model learns how to:
- read motion sensor values
- classify the motion state
- distinguish safer motion from risky motion
- support the idea of stable robot command generation

It does not claim perfect surgery control. It is a prototype that supports safer decision-making.

---

## 10. Expected Project Impact
This project can help with:
- understanding AI-assisted surgical motion
- demonstrating tremor awareness
- showing how sensor data can be used in robotics
- building a base for future shared-control research

---

## 11. Limitations
- It is not a certified medical device.
- It does not control a real robot.
- It uses a dataset from Kaggle and a demo dashboard.
- It is designed for learning, demonstration, and research.

---

## 12. Recommended Development Order
If you are building the project step by step, use this order:
1. Put the dataset in `data/raw/Dataset.csv`.
2. Run preprocessing and dataset splitting.
3. Train the classifier.
4. Evaluate the saved model.
5. Run the Flask dashboard.
6. Present the dashboard with the report.

---

## 13. How to Run the Project
### Train
```powershell
.\.venv\Scripts\python.exe training\train.py --epochs 10
```

### Evaluate
```powershell
.\.venv\Scripts\python.exe training\evaluate.py
```

### Run dashboard
```powershell
.\.venv\Scripts\python.exe dashboard\app.py
```

### Open in browser
- `http://127.0.0.1:5000`

---

## 14. Short Explanation for Presentation
DeepStable is an AI-based project that uses a sensor dataset to learn motion patterns, classify motion stability, and display the result in a live dashboard. It helps demonstrate how AI can support safer motion decisions in robotic surgery.

---

## 15. One-Line Summary
DeepStable converts raw motion sensor data into a safer AI-assisted motion decision and shows the result in a live dashboard.
