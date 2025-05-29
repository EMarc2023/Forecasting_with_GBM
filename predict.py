"""This is script to run the ML prediction for taxi demand forecasting"""

import pandas as pd
import numpy as np
import joblib
import sys


def prepare_input(
    datetime_string, best_df, median_passenger_count, median_trip_distance
):
    """The user input is a datetime_string YYYY-MM-DD HH:MM:SS.
    This function adds the additional features (to match the training data) to the user input.
    """

    try:
        date_time = pd.to_datetime(datetime_string)
    except ValueError:
        print("Invalid date and time format.")
        sys.exit(1)  # Add this line.
        return None

    features = {
        "trip_distance": median_trip_distance,
        "passenger_count": int(median_passenger_count),
        "year": np.int32(date_time.year),
        "month": np.int32(date_time.month),
        "day": np.int32(date_time.day),
        "hour": np.int32(date_time.hour),
        "dayofweek": np.int32(date_time.dayofweek),
        "is_weekend": int(date_time.dayofweek >= 5),
    }

    # Calculate lag values
    lag_24_time = date_time - pd.Timedelta(hours=24)
    lag_168_time = date_time - pd.Timedelta(hours=168)
    lag_8760_time = date_time - pd.Timedelta(hours=8760)

    lag_24_value = best_df[best_df["pickup_hour"] == lag_24_time]["trip_volume"].values
    lag_168_value = best_df[best_df["pickup_hour"] == lag_168_time][
        "trip_volume"
    ].values
    lag_8760_value = best_df[best_df["pickup_hour"] == lag_8760_time][
        "trip_volume"
    ].values

    # Handle missing lag values (if any)
    features["lag_24"] = float(lag_24_value[0] if len(lag_24_value) > 0 else 0)
    features["lag_168"] = float(lag_168_value[0] if len(lag_168_value) > 0 else 0)
    features["lag_8760"] = float(lag_8760_value[0] if len(lag_8760_value) > 0 else 0)

    input_df = pd.DataFrame([features])

    # Convert columns to the correct data types
    input_df["year"] = input_df["year"].astype(np.int32)
    input_df["month"] = input_df["month"].astype(np.int32)
    input_df["day"] = input_df["day"].astype(np.int32)
    input_df["hour"] = input_df["hour"].astype(np.int32)
    input_df["dayofweek"] = input_df["dayofweek"].astype(np.int32)
    input_df["lag_24"] = input_df["lag_24"].astype(np.float64)
    input_df["lag_168"] = input_df["lag_168"].astype(np.float64)
    input_df["lag_8760"] = input_df["lag_8760"].astype(np.float64)

    return input_df


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict.py 'YYYY-MM-DD HH:MM:SS'")
        sys.exit(1)

    datetime_string = sys.argv[1]

    try:
        # Loading the dataframe that gave the best performance for XGBoost.
        # This dataframe is needed for calculating the lag features.
        best_df = pd.read_csv("best_df.csv")
        best_df["pickup_hour"] = pd.to_datetime(best_df["pickup_hour"])

        best_model = joblib.load("best_model_reloaded.joblib")

        median_passenger_count = best_df["passenger_count"].median()
        median_trip_distance = best_df["trip_distance"].median()

        input_df = prepare_input(
            datetime_string, best_df, median_passenger_count, median_trip_distance
        )

        if input_df is not None:
            prediction = best_model.predict(input_df)
            print(f"Predicted trip volume (taxi demand) is: {prediction[0]:.2f}")
        else:
            print("Invalid date and time format.")

    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
