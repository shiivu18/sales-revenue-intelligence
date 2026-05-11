# Sales & Revenue Intelligence Platform

An end-to-end analytics and machine learning platform built using Python, SQLite, SQL, and Streamlit to analyze retail sales data, predict customer churn, segment customers, and forecast future revenue.

---

# Project Overview

This project transforms raw retail transaction data into actionable business intelligence.

The platform includes:

* Sales analytics
* Customer segmentation
* Churn prediction
* Revenue forecasting
* Interactive business dashboard
* SQL-based analytics pipeline
* Machine learning models

The system was designed to simulate a real-world analytics workflow used in modern data-driven companies.

---

# Features

## Business Analytics

* Year-over-Year (YoY) revenue analysis
* Monthly sales trends
* Region-wise revenue analysis
* Customer lifetime value analysis
* Product/category performance tracking

## Machine Learning

### Customer Churn Prediction

* Random Forest classifier
* Behavioral churn engineering
* Probability-based risk scoring

### Customer Segmentation

* RFM analysis
* KMeans clustering
* Customer intelligence profiling

### Revenue Forecasting

* Time-series feature engineering
* Lag features
* Rolling averages
* Revenue trend prediction

## Dashboard

Interactive Streamlit dashboard with:

* KPI cards
* Customer segment explorer
* Revenue visualization
* Forecast charts
* Downloadable datasets
* Interactive filters

---

# Tech Stack

## Languages

* Python
* SQL

## Libraries

* pandas
* numpy
* matplotlib
* plotly
* seaborn
* scikit-learn
* streamlit
* sqlite3

## Machine Learning

* RandomForestClassifier
* KMeans
* LinearRegression

## Database

* SQLite

---

# Project Structure

```text
sales-revenue-intelligence/
│
├── dashboard/
│   └── app.py
│
├── data/
│   ├── raw/
│   └── processed/
│       ├── customer_segments.csv
│       └── monthly_revenue.csv
│
├── notebooks/
│   └── analysis.ipynb
│
├── reports/
│
├── screenshots/
│
├── requirements.txt
│
└── README.md
```

---

# Machine Learning Pipeline

## 1. Data Cleaning

* Missing value handling
* Schema normalization
* Date conversion
* SQLite integration

## 2. Feature Engineering

### RFM Features

* Recency
* Frequency
* Monetary value

### Additional Features

* Customer tenure
* Purchase velocity
* Category diversity
* Average order value

## 3. Churn Label Engineering

Customers are classified as churned if they have not purchased within the last 180 days.

## 4. Model Training

### Churn Model

* Random Forest Classifier
* Feature importance analysis
* ROC-AUC evaluation

### Segmentation

* KMeans clustering
* Customer profile generation

### Forecasting

* Time-series feature engineering
* Lag features
* Rolling averages
* Revenue prediction

---

# Dashboard Preview

The Streamlit dashboard provides:

* Executive KPI overview
* Churn risk distribution
* Customer segmentation analysis
* Revenue forecasting
* Interactive business insights

---

# Installation

## Clone Repository

```bash
git clone <your-github-repo-url>
cd sales-revenue-intelligence
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Run Dashboard

```bash
streamlit run dashboard/app.py
```

---

# Example Insights

* Identified high-risk churn customers using behavioral analytics
* Forecasted monthly business revenue trends
* Segmented customers into business-driven behavioral groups
* Engineered ML-ready customer intelligence features
* Built an end-to-end analytics workflow from raw data to deployment

---

# Future Improvements

* XGBoost forecasting
* Advanced churn modeling
* Real-time analytics
* Cloud deployment
* API integration
* Authentication system
* Automated retraining pipeline

---

# Learning Outcomes

This project demonstrates:

* Data analytics
* SQL querying
* Data engineering
* Feature engineering
* Machine learning
* Dashboard development
* Time-series analytics
* Business intelligence workflows

---

# Author

Shiva Kumara N.

Engineering Student | Data Analytics & Machine Learning Enthusiast
