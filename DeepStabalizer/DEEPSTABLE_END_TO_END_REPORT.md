# DeepStable End-to-End Project Report

## 1. Project Title
**DeepStable: AI-Assisted Motion Stabilization Prototype for Robotic Surgical Assistance**

## 2. Abstract
DeepStable is an AI-based motion stabilization prototype that uses a Kaggle tremor dataset to train a sensor classifier for motion-state prediction. The project is designed to demonstrate how motion sensor readings can be cleaned, normalized, split into train/validation/test sets, used to train a compact neural network, and then deployed through a Flask dashboard. The system shows raw sensor motion, predicted intent or stability state, tremor level, safe robot command, and risk score. The current implementation is a research and demonstration prototype, not a certified medical device.

## 3. Project Objective
The goal of the project is to show how AI can assist motion understanding for robotic surgery-related applications. The project aims to:
- load and clean the Kaggle tremor dataset
- train a classifier on motion sensor data
- evaluate the model on unseen test data
- save a reusable checkpoint and scaler
- expose predictions through an inference wrapper
- show the result on a live dashboard

## 4. Problem Statement
Human hand motion is not perfectly stable. In robotics and surgical assistance, noisy motion or tremor can reduce precision. The project addresses this by learning motion patterns from sensor data and converting them into a safer classification output. Instead of directly controlling a real robot, the system demonstrates how motion state can be estimated and visualized in a controlled software prototype.

## 5. Project Overview
The project follows a complete pipeline:
1. A Kaggle dataset is placed in `data/raw/Dataset.csv`.
2. The dataset loader reads nine sensor features and one target label.
3. Invalid values are removed.
4. The data is split into training, validation, and test sets.
5. A normalizer is fitted on the training data.
6. A neural classifier is trained with class weighting and early stopping.
7. The best checkpoint and fitted scaler are saved.
8. The saved model is evaluated on the test split.
9. The inference utility loads the checkpoint and scaler for new readings.
10. The Flask dashboard displays motion state and risk information.

## 6. Dataset Description
The project uses the Kaggle tremor dataset, which contains the following columns:
- `aX`, `aY`, `aZ` - accelerometer values
- `gX`, `gY`, `gZ` - gyroscope values
- `mX`, `mY`, `mZ` - motion-related values
- `Result` - class label

### Dataset statistics observed during training
- Total samples: 27,995
- Classes: 2
- Class 0 count: 12,749
- Class 1 count: 15,246

This indicates a moderately imbalanced binary classification problem, which is why the trainer uses inverse-frequency class weighting.

## 7. Data Loading and Cleaning
The data loading logic is implemented in [training/dataset.py](training/dataset.py).

### Main responsibilities
- verify that the dataset file exists
- read the CSV using pandas
- check that all expected columns are present
- remove rows containing NaN or Inf values
- encode labels as integer classes if needed
- print class counts for transparency

### Cleaning behavior
The loader keeps only the nine sensor features and the `Result` label. Any rows with invalid values are dropped before training so that the model receives clean numeric input.

## 8. Train/Validation/Test Split
The dataset is split using stratified sampling so class balance is preserved across splits.

### Split ratios used by the trainer
- Validation ratio: 0.15
- Test ratio: 0.15
- Training split: remaining 0.70

### Why stratification matters
Because the dataset is binary and slightly imbalanced, stratified splitting prevents one split from accidentally containing too many samples of one class. That gives a more reliable performance estimate.

## 9. Normalization and Preprocessing
The normalization logic is implemented in [preprocessing/normalise.py](preprocessing/normalise.py).

### What it does
- fits a mean and standard deviation on the training split only
- applies the same transform to validation and test data
- avoids division by zero for constant features
- saves the fitted scaler to `model/scaler.pkl`

### Why normalization is needed
The sensor columns have different numeric ranges. Standardization improves optimization stability and helps the model converge faster.

## 10. Model Architecture
The classifier is defined in [model/sensor_classifier.py](model/sensor_classifier.py).

### Architecture summary
- Input: 9 features
- BatchNorm1d
- Linear(64) + GELU + Dropout
- BatchNorm1d
- Linear(128) + GELU + Dropout
- BatchNorm1d
- Linear(64) + GELU + Dropout
- Final Linear layer to output class logits

### Design purpose
This is a compact multilayer perceptron optimized for tabular sensor input. It is small enough to train quickly on a CPU while still being expressive enough to capture motion-state patterns.

### Model output
The model produces class logits, which are converted to class probabilities during inference.

## 11. Training Pipeline
The training pipeline is implemented in [training/train.py](training/train.py).

### Training steps
1. Load the dataset.
2. Split the data into training, validation, and test sets.
3. Fit the normalizer on training data.
4. Save the scaler.
5. Save the test split as `.npy` files for later evaluation.
6. Create DataLoader objects for training and validation.
7. Build the classifier.
8. Compute inverse-frequency class weights.
9. Use CrossEntropyLoss with weighted classes.
10. Train with AdamW.
11. Reduce learning rate on validation loss plateaus.
12. Apply early stopping when validation loss stops improving.
13. Save the best checkpoint.
14. Save training history as JSON.

### Training configuration
- Epochs default: 50
- Batch size default: 128
- Learning rate default: 3e-4
- Weight decay: 1e-4
- Dropout: 0.3
- Patience: 10

### Why this training design is effective
- class weighting improves learning on imbalanced data
- early stopping reduces overfitting
- validation monitoring prevents unnecessary epochs
- checkpointing preserves the best model

### Files created during training
- `model/sensor_classifier.pth`
- `model/scaler.pkl`
- `model/X_test.npy`
- `model/y_test.npy`
- `model/training_history.json`

## 12. Evaluation Pipeline
The evaluation logic is implemented in [training/evaluate.py](training/evaluate.py).

### What evaluation does
- loads the saved checkpoint
- loads the saved test split
- runs inference on the test data
- computes standard classification metrics
- saves a JSON report in the `reports` folder

### Metrics reported
- Accuracy
- Precision
- Recall
- F1 Score
- Balanced Accuracy
- Specificity
- Confusion matrix
- Classification report

### Final evaluation result from the trained model
- Accuracy: 86.43%
- Precision: 1.0000
- Recall: 0.7508
- F1 Score: 0.8576
- Balanced Accuracy: 0.8754
- Specificity: 1.0000

### Confusion matrix
- True negatives: 1913
- False positives: 0
- False negatives: 570
- True positives: 1717

These results show strong precision and specificity, with a lower recall on the positive class. That means the model is conservative and avoids false alarms, while still identifying a large portion of the positive cases.

## 13. Inference Layer
The inference wrapper is implemented in [inference.py](inference.py).

### Role of the inference class
`DeepStablePredictor` provides a reusable API for prediction on new sensor readings.

### What it loads
- saved checkpoint from `model/sensor_classifier.pth`
- saved scaler from `model/scaler.pkl`

### Prediction workflow
1. Accept a single sensor reading or a batch.
2. Normalize the input using the saved scaler.
3. Run the classifier in evaluation mode.
4. Return the predicted class, label, risk score, and probabilities.

### Default label mapping
- `0` → stable
- `1` → unstable

This makes the model output easy to interpret in the dashboard and in reports.

## 14. Dashboard and Live Visualization
The dashboard backend is implemented in [dashboard/app.py](dashboard/app.py), and the frontend is defined in the HTML, JavaScript, and CSS files inside the dashboard folder.

### Dashboard purpose
The dashboard provides a human-readable view of the AI result. It is not the training system itself; it is the presentation and live demonstration layer.

### Dashboard features
- live raw sensor stream
- AI prediction label
- tremor level
- safe robot command
- risk score
- history buffer for recent states

### API endpoints
- `/` → renders the dashboard page
- `/api/state` → returns the current live system state
- `/api/predict` → accepts sensor values and returns a prediction

### Dashboard behavior
- a background thread simulates or receives live sensor updates
- if a trained model is available, predictions are generated through the inference layer
- if not, the app can fall back to demo behavior

## 15. Current Project Structure
The key files in the final active project are:
- [training/dataset.py](training/dataset.py)
- [training/train.py](training/train.py)
- [training/evaluate.py](training/evaluate.py)
- [preprocessing/normalise.py](preprocessing/normalise.py)
- [model/sensor_classifier.py](model/sensor_classifier.py)
- [inference.py](inference.py)
- [dashboard/app.py](dashboard/app.py)
- [dashboard/templates/dashboard.html](dashboard/templates/dashboard.html)
- [dashboard/static/dashboard.js](dashboard/static/dashboard.js)
- [dashboard/static/style.css](dashboard/static/style.css)

## 16. Dependencies
The project depends on:
- torch
- numpy
- pandas
- scikit-learn
- flask

These are listed in [requirements.txt](requirements.txt).

## 17. How to Run the Project
### 17.1 Activate the virtual environment
```powershell
.\.venv\Scripts\Activate.ps1
```

### 17.2 Install dependencies
```powershell
pip install -r requirements.txt
```

### 17.3 Train the model
```powershell
python training/train.py --epochs 50
```

### 17.4 Evaluate the model
```powershell
python training/evaluate.py
```

### 17.5 Run the dashboard
```powershell
python dashboard/app.py
```

### 17.6 Open in browser
```text
http://127.0.0.1:5000
```

## 18. What the Project Outputs
The project produces both machine learning outputs and user-facing outputs.

### Machine learning outputs
- trained classifier checkpoint
- fitted scaler
- evaluation JSON report
- test split arrays

### User-facing outputs
- dashboard with live sensor state
- readable AI predictions
- risk score and safe command indicator
- explanation of whether the motion is stable or unstable

## 19. Real-World Meaning
This project does not directly control a real surgical robot. Instead, it demonstrates the software pipeline that could sit before robot motion execution. In a more advanced system, the classifier output or risk score could be used as part of a safety layer, shared-control module, or decision-support system.

## 20. Impact
The project is useful because it:
- demonstrates AI for medical robotics concepts
- shows end-to-end data processing from CSV to dashboard
- provides a reproducible training pipeline
- gives a visually understandable motion-risk demo
- creates a base for future research or extension

## 21. Limitations
The current project has the following limitations:
- it is not a certified medical device
- it does not connect to real hospital robot hardware
- it uses a single Kaggle dataset
- it is optimized for demonstration and learning
- recall is lower than precision, so some positive cases are missed

## 22. Future Improvements
Possible future improvements include:
- collecting more motion datasets
- adding stronger feature engineering
- testing more advanced models
- improving recall for the positive class
- making the dashboard more interactive
- connecting the classifier to a robot simulator
- adding clinical-style validation and confidence intervals

## 23. Conclusion
DeepStable is a complete AI-assisted motion stabilization prototype that transforms a Kaggle tremor dataset into a trained classifier, an evaluation report, and a live dashboard. The project demonstrates the full software workflow from dataset loading and cleaning to training, testing, inference, and visualization. It is suitable for academic presentation, project submission, and as a base for future robotic safety research.

## 24. Short Viva Summary
DeepStable is an AI-based motion stabilization project that trains a classifier on a Kaggle sensor dataset, evaluates it with standard metrics, and shows the output in a live dashboard as raw motion, prediction, tremor level, safe robot command, and risk score.