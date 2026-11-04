# 🌍 AirSource – Air Quality Monitoring & Source Attribution

**Hackathon:** Neural Storm 2026  
**Track:** Green Planet  
**Problem Statement:** GP-01 – Air Quality Monitoring & Source Attribution

## 1. Project Overview

AirSource is an air-quality monitoring prototype designed to help users understand pollution levels and explore possible pollution sources.

The project combines an interactive web dashboard with a Python-based data analysis and machine-learning component.

It aims to make air-quality information easier to understand and support environmental awareness.

## 2. Problem Statement

Air pollution is a major environmental challenge. Pollutants such as PM2.5, PM10, NO2, SO2, CO and O3 affect air quality and human health.

AirSource aims to provide an accessible platform for monitoring pollutant readings, analysing historical air-quality data and exploring possible pollution sources.

## 3. Key Features

- Air Quality Index (AQI) dashboard.
- PM2.5 and PM10 monitoring.
- NO2, SO2, CO and O3 readings.
- Historical air-quality trend visualisation.
- Pollution-source indicators.
- AQI-based health recommendations.
- Python-based machine-learning component for AQI category classification.
- Interactive data visualisation.

## 4. Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend / Analysis | Python |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas |
| Visualisation | Plotly |
| Dashboard | Streamlit |
| Model Storage | Joblib |

## 5. Dataset

The project uses the India Air Quality Dataset as its intended historical data source.

Dataset link: https://www.kaggle.com/datasets/rohanrao/air-quality-data-in-india

The dataset contains historical air-quality measurements from Indian monitoring stations.

The Python training script expects these columns:

- PM2.5
- PM10
- NO2
- SO2
- CO
- O3
- AQI_Bucket

Download the dataset and place the CSV file at:

`data/air_quality.csv`

**Note:** The dataset must be downloaded separately. The repository does not currently include the dataset file.

## 6. Machine Learning

The Python component includes a Random Forest classification pipeline.

Its intended task is to classify AQI categories using pollutant measurements.

The training script uses:
- Random Forest Classifier.
- Missing-value imputation.
- Training and testing split.
- Accuracy evaluation.
- Macro F1-score.
- Classification report.

Run the training script after downloading the dataset:

`python train_model.py`

The actual evaluation metrics will be generated in `models/metrics.json`.

No accuracy result is claimed until the model has been trained and evaluated.

## 7. Pollution Source Attribution

The existing dashboard uses predefined pollutant-based rules to explore possible pollution sources.

The indicators include:
- Traffic-related pollution.
- Industrial and combustion-related pollution.
- Dust-related pollution.
- Biomass-burning-related scenarios.
- Secondary pollution indicators.

**Important:** These are exploratory, rule-based estimates. They are not scientifically validated source-apportionment measurements.

The AQI classification model does not independently identify pollution sources.

## 8. Project Structure

```text
Air-Quality-Indexing/
│
├── index.html
├── README.md
├── app.py
├── train_model.py
├── requirements.txt
├── .gitignore
├── SUBMISSION_CHECKLIST.md
│
├── data/
│   └── README.md
│
├── models/
└── screenshots/
```

## 9. Installation and Execution

### Requirements

- Python 3.10 or newer.
- pip package manager.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Download the dataset

Download the CSV from the Kaggle dataset link and save it as:

`data/air_quality.csv`

### Train the model

```bash
python train_model.py
```

### Launch the Python dashboard

```bash
streamlit run app.py
```

### Open the original web dashboard

Open `index.html` in a modern web browser.

## 10. Current Limitations

The current prototype has the following limitations:

- The original HTML dashboard uses simulated readings.
- Historical data must be downloaded separately.
- Real-time sensor integration is not implemented.
- Satellite imagery integration is not implemented.
- Pollution-source estimates are rule-based and exploratory.
- The machine-learning model must be trained and evaluated before use.

## 11. Future Enhancements

- Integration with real-time air-quality APIs.
- Integration of ground monitoring station data.
- Satellite-based pollution observation.
- Wind direction and meteorological analysis.
- Geographical pollution mapping.
- Validated machine-learning source-attribution methods.
- Improved AQI forecasting.

## 12. Team Information

**Team Name:** [Enter registered team name]

**Team Members:**
1. Busarapalli Datta Sai Team Leader
2. Konne Sai Deekshitha
3. Yeswanth K R

## 13. AI Tools Disclosure

The initial HTML dashboard and README were generated with assistance from Claude.

ChatGPT was used to assist with project planning and preparation of the Python implementation scaffold.

The team is responsible for reviewing, testing and understanding all submitted code.

Update this disclosure to reflect all tools actually used.

## 14. Project Purpose

AirSource is an educational environmental technology prototype intended to improve awareness of air pollution through data analysis, visualisation and machine-learning experimentation.

It is not an official air-quality warning system or a substitute for government monitoring services.

---

**Project:** AirSource  
**Track:** Green Planet – GP-01  
**Hackathon:** Neural Storm 2026
