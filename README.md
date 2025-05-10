
Taxi Fare Prediction API

A production-ready project for predicting taxi fares using a FastAPI backend, trained ML models (XGBoost, CatBoost), and a custom preprocessing pipeline. The project includes Dockerized deployment, PostgreSQL integration, and a modular codebase.

📌 Features
REST API built with FastAPI

Feature engineering & preprocessing pipeline

Modular ML model integration (XGBoost, CatBoost, Scikit-learn)

Dockerized for production use

Optional Streamlit dashboard for interaction

PostgreSQL-ready data pipeline

🧠 Machine Learning Workflow
🔍 Feature Engineering Includes:
Feature	Description
| Feature                  | Description                                 |
| ------------------------ | ------------------------------------------- |
| `trip_distance`          | Calculated from Haversine distance          |
| `pickup_hour`, `weekday` | Extracted from timestamp                    |
| `rush_hour_flag`         | Binary indicator for traffic-heavy hours    |
| `log_fare`               | Log-transform of target variable (optional) |
| `price_per_km`           | Target/Distance to normalize by trip size   |
and more feature engineering including distance from most important place in new york like airports and this feature engineering boost my model very much


