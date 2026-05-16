# Nifty 100 Intelligence System

A full-stack financial intelligence platform designed to evaluate and analyze the top 100 companies. The system calculates comprehensive ML health scores, detects anomalies, identifies financial trends, and displays insights on a dynamic, premium React dashboard.

## 🚀 Features

- **Dynamic Financial Dashboard**: A modern, glassmorphism-styled UI built with React, Vite, and Recharts. Includes interactive views for ML Scores, Anomalies, and detailed company metrics.
- **ML Health Scoring**: A Python-based ML Engine that scores companies based on 6 key dimensions: Profitability, Growth, Leverage, Cash Flow, Dividend Track Record, and Growth Trend.
- **Automated Pros & Cons Engine**: An automated rule engine that parses financial metrics and identifies distinct strengths and weaknesses for each company.
- **FastAPI Backend**: A lightning-fast REST API powered by FastAPI and SQLAlchemy, serving real-time insights to the frontend.
- **Automated Data Pipelines**: Celery task pipelines designed to automatically execute ETL processes, populate the database, and run the ML models.
- **Jupyter Data Science Suite**: A collection of generated notebooks for Exploratory Data Analysis, Anomaly Detection, Sector Clustering, and Peer Comparison.

## 🛠️ Technology Stack

- **Frontend**: React.js, Vite, Recharts, Lucide-React
- **Backend API**: FastAPI, Uvicorn, SQLAlchemy
- **Database**: SQLite (Configured for easy local setup, easily extensible to PostgreSQL)
- **ML & Data Processing**: Pandas, Scikit-Learn, Celery, Redis
- **Data Visualization**: Jupyter Notebooks, Plotly, Seaborn, Matplotlib

## 📂 Project Structure

```
.
├── api/                  # FastAPI backend and SQLAlchemy models/database config
├── dashboard/            # Vite + React frontend application
├── ml_engine/            # Celery tasks and ML scoring algorithms
├── notebooks/            # Jupyter notebooks for interactive data science
├── generate_notebooks.py # Script to scaffold Jupyter notebooks
└── requirements.txt      # Python dependencies
```

## ⚙️ Getting Started

### 1. Backend Setup

First, install the required Python dependencies:
```bash
pip install -r requirements.txt
```

Generate the SQLite database and run the ML Engine to seed the initial data:
```bash
python -c "import sys; sys.path.append('.'); from ml_engine.tasks import run_etl_pipeline, score_all_companies, generate_pros_cons; run_etl_pipeline(); score_all_companies(); generate_pros_cons();"
```

Start the FastAPI development server:
```bash
uvicorn api.main:app --reload
```
*The API will be available at `http://localhost:8000`*

### 2. Frontend Setup

In a new terminal window, navigate to the dashboard directory and install the Node modules:
```bash
cd dashboard
npm install
```

Start the Vite development server:
```bash
npm run dev
```
*The dashboard will be available at `http://localhost:5173`*

## 🔮 Future Enhancements
- Integration of a real-time Redis cache for Celery ML task scheduling
- Migration from SQLite to a fully managed PostgreSQL database
- Advanced Peer Comparison logic in the dashboard
