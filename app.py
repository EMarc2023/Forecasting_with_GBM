import streamlit as st
import pandas as pd
import numpy as np
import joblib
from datetime import timedelta

@st.cache_resource
def load_resources():
    """Load model and best_df once"""
    best_df = pd.read_csv("best_df.csv")
    best_df["pickup_hour"] = pd.to_datetime(best_df["pickup_hour"])
    model = joblib.load("best_model_reloaded.joblib")
    average_passenger_count = best_df["passenger_count"].mean()
    average_trip_distance = best_df["trip_distance"].mean()
    average_fare_amount = best_df["fare_amount"].mean()
    average_total_amount = best_df["total_amount"].mean()
    return model, best_df, average_passenger_count, average_trip_distance, \
        average_fare_amount, average_total_amount

model, best_df, average_passenger_count, average_trip_distance, average_fare_amount, \
    average_total_amount = load_resources()

def prepare_input(datetime_string):
    """Prepare input DataFrame for prediction"""
    try:
        date_time = pd.to_datetime(datetime_string)
    except ValueError:
        return None

    features = {
        "trip_distance": average_trip_distance,
        "fare_amount": average_fare_amount,
        "total_amount": average_total_amount,
        "passenger_count": int(average_passenger_count),
        "year": np.int32(date_time.year),
        "month": np.int32(date_time.month),
        "day": np.int32(date_time.day),
        "hour": np.int32(date_time.hour),
        "dayofweek": np.int32(date_time.dayofweek),
        "is_weekend": int(date_time.dayofweek >= 5),
    }

    # Lag features
    for lag, hours in zip(["lag_24", "lag_168", "lag_8760"], [24, 168, 8760]):
        lag_time = date_time - timedelta(hours=hours)
        lag_value = best_df[best_df["pickup_hour"] == lag_time]["trip_volume"].values
        features[lag] = float(lag_value[0] if len(lag_value) > 0 else 0)

    input_df = pd.DataFrame([features])
    return input_df

# Streamlit UI
st.title("NYC Yellow Taxi Demand Forecasting")
st.write("📊 Predict trip volume using a trained machine learning model.")

datetime_input = st.text_input("Enter date and hour (YYYY-MM-DD HH:MM:SS), with no quotation marks", "")

if st.button("Predict"):
    if datetime_input.strip() == "":
        st.error("Please enter a valid datetime string.")
    else:
        input_df = prepare_input(datetime_input)
        if input_df is None:
            st.error("Invalid date and time format. Use YYYY-MM-DD HH:MM:SS.")
        else:
            prediction = model.predict(input_df)
            st.success(f"🟡 Predicted trip volume is: **{prediction[0]:.2f}**")
