# 🌡️ Urban Heat Stress Hotspot Detection

> 🌍 **An AI-powered geospatial intelligence system for detecting, predicting, and mitigating urban heat stress hotspots using satellite-derived indicators, environmental factors, and machine learning.**

Developed as part of **Bharatiya Antariksha Hackathon 2026**, this project integrates Remote Sensing, GIS, Artificial Intelligence, and Data Analytics to support climate-resilient urban planning and sustainable city development.

---

# 🚀 Project Overview

Rapid urbanization has intensified the **Urban Heat Island (UHI)** effect, causing cities to experience significantly higher temperatures than surrounding regions. These elevated temperatures impact public health, energy consumption, infrastructure, and overall quality of life.

This project develops an end-to-end geospatial AI framework capable of:

* 🔍 Detecting Urban Heat Stress Hotspots
* 📊 Identifying drivers of urban heating
* 🤖 Predicting Land Surface Temperature (LST)
* 🧠 Explaining model predictions using Explainable AI
* 🌱 Evaluating heat mitigation strategies
* 🔄 Simulating future urban planning scenarios

The framework combines environmental, geographical, and socio-economic indicators to provide actionable insights for urban planners and decision-makers.

---

# 🎯 Objectives

### Primary Goals

✅ Detect Urban Heat Stress Hotspots

✅ Analyze environmental and urban factors contributing to heat accumulation

✅ Predict Land Surface Temperature (LST)

✅ Explain model predictions using Explainable AI

✅ Evaluate mitigation strategies through scenario-based simulations

✅ Support climate-resilient urban planning

---

# 🌍 Study Area

**Chhatrapati Sambhajinagar (Aurangabad), Maharashtra, India**

The city serves as a case study for analyzing Urban Heat Island effects and identifying heat-vulnerable regions using geospatial intelligence and machine learning techniques.

---

# 📊 Dataset Version 2

### Environmental Features

* 🌿 NDVI (Normalized Difference Vegetation Index)
* 🏙️ NDBI (Normalized Difference Built-up Index)
* ⛰️ Elevation
* 👥 Population Density

### Spatial Features

* 📍 Latitude
* 📍 Longitude

### Target Variable

* 🌡️ Land Surface Temperature (LST)

---

# ⚙️ Feature Engineering

The following engineered features were developed to enhance model interpretability and analysis:

* Green_Built_Ratio
* Population_Heat_Index
* Elevation_Cooling_Index

These features capture interactions between vegetation, urbanization, elevation, and population characteristics.

---

# 🧠 Machine Learning Pipeline

### Data Processing

* Data Audit
* Data Cleaning
* Exploratory Data Analysis (EDA)
* Correlation Analysis
* Feature Engineering

### Machine Learning Models

* Linear Regression (Baseline Model)
* Random Forest Regressor
* XGBoost Regressor

### Explainable AI

* Feature Importance Analysis
* SHAP-Based Model Interpretation

### Classification

* Urban Heat Hotspot Detection

### Decision Support

* Scenario-Based Heat Mitigation Simulation

---

# 📈 Model Performance

| Model                        | Performance       |
| ---------------------------- | ----------------- |
| Linear Regression (Baseline) | R² ≈ 0.49         |
| Random Forest                | R² ≈ 0.68         |
| XGBoost                      | R² ≈ 0.71         |
| Hotspot Detection            | Accuracy ≈ 82.36% |

### Best Performing Model

🏆 **XGBoost Regressor**

* R² ≈ 0.71
* MAE ≈ 1.40
* RMSE ≈ 1.78

---

# 🔍 Key Findings

* Higher NDBI values are associated with increased urban heat.
* Vegetation (NDVI) contributes to cooling effects.
* Built-up regions exhibit higher Land Surface Temperatures.
* Elevation influences local temperature variations.
* Urban Heat Hotspots can be identified with over 82% accuracy.
* Scenario simulations support data-driven urban heat mitigation planning.

---

# 🛠️ Technology Stack

## Programming & Data Science

* Python
* Pandas
* NumPy

## Machine Learning

* Scikit-Learn
* Random Forest
* XGBoost
* SHAP

## Geospatial Technologies

* Google Earth Engine
* QGIS
* Remote Sensing Datasets

## Visualization

* Matplotlib
* Streamlit

## Development Tools

* Git
* GitHub
* Jupyter Notebook
* VS Code

---

# 📂 Project Structure

```text
UrbanHeatStress/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_audit.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_feature_engineering.ipynb
│   ├── 05_model_baseline.ipynb
│   ├── 06_hotspot_detection.ipynb
│   ├── 07_explainable_ai.ipynb
│   ├── 08_scenario_simulation.ipynb
│   ├── 09_random_forest.ipynb
│   └── 10_xgboost.ipynb
│
├── outputs/
│   ├── plots/
│   └── reports/
│
├── src/
│   ├── cleaning.py
│   ├── eda.py
│   ├── features.py
│   ├── hotspot.py
│   ├── model.py
│   └── utils.py
│
├── README.md
└── requirements.txt
```

---

# 🔄 Project Workflow

```text
Satellite Data Collection
            ↓
GIS Processing
            ↓
NDVI / NDBI / LST Extraction
            ↓
Dataset Preparation
            ↓
Data Cleaning
            ↓
Exploratory Data Analysis
            ↓
Feature Engineering
            ↓
Baseline Model
            ↓
Random Forest
            ↓
XGBoost
            ↓
Heat Stress Prediction
            ↓
Hotspot Detection
            ↓
Explainable AI
            ↓
Scenario Simulation
            ↓
Dashboard & Visualization
```

---

# 📓 Notebook Pipeline

| Notebook                     | Description                                 |
| ---------------------------- | ------------------------------------------- |
| 01_data_audit.ipynb          | Data inspection and quality assessment      |
| 02_data_cleaning.ipynb       | Data preprocessing and cleaning             |
| 03_eda.ipynb                 | Exploratory Data Analysis                   |
| 04_feature_engineering.ipynb | Feature creation and transformation         |
| 05_model_baseline.ipynb      | Linear Regression baseline model            |
| 06_hotspot_detection.ipynb   | Urban heat hotspot classification           |
| 07_explainable_ai.ipynb      | Feature importance and model interpretation |
| 08_scenario_simulation.ipynb | Urban heat mitigation simulations           |
| 09_random_forest.ipynb       | Random Forest temperature prediction        |
| 10_xgboost.ipynb             | XGBoost temperature prediction              |

---

# 🌱 Scenario Simulation

The framework evaluates potential mitigation strategies through scenario-based analysis:

* Increasing vegetation cover (NDVI)
* Reducing built-up intensity (NDBI)
* Assessing resulting temperature changes

This enables planners to evaluate interventions before implementation.

---

# 👥 Team

This project is being developed by a multidisciplinary team participating in **Bharatiya Antariksha Hackathon 2026**.

### 🌍 Srushti Bawaskar

**Geospatial & Data Lead**

### 👩‍💻 Priyal Deshmukh

**AI/ML Lead**

### 📊 Rishika Deshmukh

**Research, Dashboard & Documentation Lead**

---

# 🌱 Expected Impact

The proposed system can support:

* Climate-Resilient Urban Planning
* Smart City Development
* Heat Risk Assessment
* Sustainable Infrastructure Planning
* Environmental Decision Support Systems

By identifying vulnerable heat-stress regions and evaluating mitigation strategies, the project contributes toward creating safer and more sustainable urban environments.

---

# 🔮 Future Enhancements (Version 3)

Planned enhancements include:

* Land Cover Integration
* Road Density Analysis
* Water Proximity Analysis
* Nighttime Light Data
* Interactive GIS-Based Heat Maps
* Real-Time Satellite Data Integration
* Climate Risk Forecasting Dashboard
* Multi-City Comparative Analysis

---

# 🏆 Bharatiya Antariksha Hackathon 2026

This project combines **Remote Sensing**, **Geospatial Analytics**, **Artificial Intelligence**, and **Climate Science** to address one of the most critical urban sustainability challenges of our time.

---

# ⭐ Vision

**"Building climate-resilient cities through geospatial intelligence, machine learning, and data-driven decision making."** 🌍🚀🌱
