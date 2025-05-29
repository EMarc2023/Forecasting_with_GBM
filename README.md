# About this project
This project showcases demand forecasting using a gradient boosting machine learning algorithm. Demand forecasting is crucial for resource allocation analytics, pricing, and revenue optimisation.

The dataset used for this project are taken from the 2023-2024 data of the NYC yellow taxi data (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

## Executive summary
This project tackles demand forecasting for the NYC yellow taxis. In this project, I demonstrate how a simple machine learning operations (MLOps) pipeline can help us generate valuable insights and help stakeholders make effective and responsible business decisions. 

## Solution design
### For the Jupyter notebook:
```mermaid
---
config:
  layout: fixed
---
flowchart TD
    A["Jupyter Notebook"] --> B["Load data in Parquet"]
    B --> C["Exploratory data analysis"]
    C --> D["Data cleaning"]
    D --> E["Feature engineering"]
    E --> F["Forecasting with XGBoost"]
    F --> G["Choose the best model"]
    G --> H["Feature importance"]
    H --> I["Serialise best model"]
    I --> J["Derive business insights"]
```

### For `predict.py`
This script will load the best-performing model and lets users forecast taxi demand by providing a date and hour (see How to run the notebook and prediction" for details).

## Business insights and conclusions:
1. Time-series data, such as illustrated by the NYC taxi data, follows strong multi-seasonal trends. In the case of the NYC yellow taxi data, the seasonalities are daily, monthly, and yearly.

2. Understanding these seasonalities is crucial for businesses to optimise resource allocation and implement dynamic pricing strategies to maximise revenue during high-demand periods.

3. Feature importance helps businesses identify the strongest features that contribute to the observed data (e.g, in this case study, the taxi demand).

4. By including seasonality (via lag terms), we can build a higher-performing ML model for forecasting. As demonstrated in the Jupyter notebook, including the lag terms reduces the root mean square error (RMSE) by around 10% compared to the baseline model.

5. Well-practised data science and MLOps are valuable tools to enhance business outcomes.

## How to run the notebook and prediction

### Step 1
Clone this repository.

### Step 2
Install the required Python packages (listed in `requirements.txt`) if necessary. Here are the steps:
```
bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3
### Running the notebook
To run the notebook, open "Forecasting-NYC-yellow-taxi.ipynb" on a Jupyter interface and run all cells.

### Running the prediction script
To run `predict.py`, execute the following:
```
bash
python3 predict.py "YYYY-MM-DD HH:00:00"
```

Example:
Running
```
bash
python3 predict.py "2025-05-11 19:00:00"

```
will output
```
Predicted trip volume (taxi demand) is: 5134.99
```

## Limitation
This solution is best suited for short-term time-forecasting (with 1 a year time horizon), as the ML model was trained on a 2 year data with lag features of (1 day, 1 week, and 1 year - following the seasonalities).

## Production considerations and further developments
While I have provided a simple unit test (`tests/test_predict.py`) and a simple CI pipeline (for now), to turn this exercise for full-blown production workloads, I would:
1. Further refine the models by performing a more detailed hyperparameter search and explore more interaction terms (such as combining weather and the day of the week and/or holiday season and geographic area).
2. Add automated ML model retraining as new data arrives, and a data drift monitoring feature. The data drift monitoring will help both the data scientists and stakeholders, ensuring that the model adapts to seasonal trends or fluctuating taxi demand.
3. Containerise the ML prediction application (using Docker, for example) for a scalable and/or cloud deployment.   
4. Consider using scalable data handling (e.g., Dask, Spark for data wrangling, Airflow for data orchestration) if the data volume warrants it.
