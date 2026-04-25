# DeepStable Project Report

## Title
DeepStable: A Synthetic Tremor Demo and AI-Assisted Motion Stabilization Prototype for Robotic Surgical Assistance

## Abstract
DeepStable is a prototype project designed to demonstrate how surgeon hand motion can be stabilized before it is used for robotic assistance. The project focuses on understanding tremor-like motion using synthetic demo signals and showing how a model-based system can produce a smoother output signal. A Flask-based dashboard visualizes the raw motion, reference motion, filtered output, and risk-related values. The project is intended as an educational and research prototype, not as a clinical medical device.

## 1. Introduction
Robotic surgery requires highly stable motion because even small involuntary hand movements can affect precision. In real surgical settings, surgeon motion may contain tremor, noise, and instability. DeepStable demonstrates a simple AI-assisted idea to improve motion stability and make the signal easier to interpret.

This project was developed to show the basic workflow of:
- receiving motion input
- analyzing it
- reducing unwanted tremor-like variation
- displaying the result in a live dashboard

## 2. Problem Statement
Human hand motion is not perfectly steady. When motion is directly transferred to a robot, small tremors may also be transferred. This can reduce precision and increase the risk of error in delicate tasks.

The project addresses the following problem:
- how to represent motion data
- how to show tremor reduction visually
- how to build a simple AI-based stabilization prototype for demonstration

## 3. Project Objective
The main objectives of DeepStable are:
- to create a clear demonstration of motion stabilization
- to generate synthetic tremor-like signals for testing
- to train a simple model on noisy and clean motion patterns
- to display the motion output in a dashboard
- to explain how AI can support safer robotic motion

## 4. Proposed Solution
DeepStable uses a synthetic demo workflow.

### Solution Flow
1. Generate synthetic motion data.
2. Create a clean reference motion and a raw noisy motion.
3. Apply preprocessing such as bandpass filtering and normalization.
4. Use a Transformer + BiLSTM model to learn motion patterns.
5. Produce a smoother filtered output.
6. Show the result in a real-time dashboard.

### What the solution provides
- an easy-to-understand demonstration
- a visual comparison between raw and filtered motion
- a foundation for future surgical robotics research

## 5. System Modules
The project is divided into the following modules:

### 5.1 Synthetic Data Generation
This module creates demo tremor signals using mathematical functions. It helps simulate motion data without requiring real medical hardware.

### 5.2 Preprocessing
This module prepares the data by:
- removing unwanted frequency content
- normalizing values
- splitting the signal into windows

### 5.3 AI Model
The model learns from noisy input and cleaner target output. It is used to approximate a stabilized motion signal.

### 5.4 Training Module
The training code fits the model on synthetic motion samples and saves the learned weights.

### 5.5 Evaluation Module
The evaluation code computes basic metrics such as:
- RMSE
- SNR
- tremor reduction percentage

### 5.6 Dashboard Module
The dashboard displays:
- raw signal
- reference motion
- filtered output
- metric cards
- project mode label

## 6. Technology Used
- Python
- PyTorch
- NumPy
- SciPy
- Flask
- Chart.js
- HTML, CSS, JavaScript

## 7. Current Output
The current output of the project is a live dashboard that shows how motion stabilization works in demo mode.

### Output Includes
- a synthetic raw motion waveform
- a reference motion waveform
- a filtered motion waveform
- SNR values
- tremor reduction value
- risk score

## 8. Expected Impact
This project creates educational and research value by showing how AI can help stabilize motion before robotic execution. Its impact includes:
- easier understanding of surgical motion filtering
- a prototype foundation for future robotic assistance systems
- improved visualization of motion stability concepts
- a possible starting point for more advanced shared-control systems

## 9. Scope and Limitation
### Scope
- demo-level AI motion stabilization
- dashboard-based visualization
- synthetic data workflow
- prototype for academic explanation

### Limitations
- it is not a clinical medical device
- it does not control a real robot
- it uses synthetic data instead of hospital data
- it is not validated for surgical use

## 10. Future Enhancement
The project can be improved by:
- using real motion datasets
- adding better intent prediction
- adding shared control logic
- connecting to a robot simulator
- improving evaluation with more clinical-style metrics

## 11. Kaggle Dataset Training Process
The shared Kaggle dataset is used as the training source for the motion classification model.

### Dataset Columns
- aX, aY, aZ: accelerometer values
- gX, gY, gZ: gyroscope values
- mX, mY, mZ: motion-related values
- Result: binary target label

### Training Steps
1. Place `Dataset.csv` in `data/raw/` or use the shared download path.
2. Load the CSV and separate the 9 sensor features from the `Result` label.
3. Split the dataset into train, validation, and test sets.
4. Standardize the sensor features using only the training set statistics.
5. Train a small neural classifier on the sensor vectors.
6. Save the trained checkpoint and the normalization values.
7. Evaluate the model using accuracy, precision, recall, F1 score, and confusion matrix.

### What the Model Learns
- It learns to classify the sensor state from the dataset.
- The output can be used as a tremor/risk indicator in the project.
- This helps the dashboard show a safer robot command decision.

## 12. Conclusion
DeepStable is a clear and practical prototype that demonstrates how motion stabilization can be applied in a robotic surgery context. The project currently works as a synthetic demo with AI-based filtering and live visualization. It provides a strong base for future development and helps explain the overall concept in a simple and professional way.

## 13. Project Files
- `dashboard/app.py` - Flask backend for dashboard and demo data stream
- `dashboard/demo_data.py` - synthetic demo signal generator
- `dashboard/templates/dashboard.html` - UI layout
- `dashboard/static/dashboard.js` - chart update logic
- `dashboard/static/style.css` - dashboard styling
- `training/train.py` - model training script
- `training/evaluate.py` - evaluation script
- `training/loss.py` - custom loss function
- `model/deepstable_model.py` - hybrid model definition
- `preprocessing/` - preprocessing utilities

## 14. Short Viva Answer
DeepStable is a synthetic demo project that shows how AI can stabilize motion before it is used in robotic surgery. It creates noisy motion, learns a cleaner pattern, and displays raw versus filtered motion in a live dashboard.
