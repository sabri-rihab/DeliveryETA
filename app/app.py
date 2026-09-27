import streamlit as st
import pandas as pd
import joblib

# --------------------------------
# Load model and feature columns
# --------------------------------

model = joblib.load("models/randomForest_model.joblib")
feature_columns = joblib.load("models/feature_columns.joblib")


# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="Delivery Time Predictor",
    page_icon="🚚",
    layout="wide"
)

st.title("🚚 Delivery Time Predictor")
st.write("Enter the order information to predict the delivery time.")


# --------------------------------
# User inputs
# --------------------------------

col1, col2 = st.columns(2)

with col1:

    distance = st.number_input(
        "Distance (km)",
        min_value=0.0,
        max_value=25.0,
        value=5.0
    )

    weather = st.selectbox(
        "Weather",
        ["Sunny", "Stormy", "Sandstorms", "Cloudy", "Windy", "Fog"]
    )

    traffic = st.selectbox(
        "Traffic density",
        ["Low", "Medium", "High", "Jam"]
    )

    vehicle = st.selectbox(
        "Vehicle type",
        ["Motorcycle", "Scooter", "Electric Scooter"]
    )


with col2:

    festival = st.selectbox(
        "Festival",
        ["No", "Yes"]
    )

    city = st.selectbox(
        "City",
        ["Urban", "Metropolitian", "Semi-Urban"]
    )

    order_time = st.time_input(
        "Order time"
    )

    picked_time = st.time_input(
        "Order picked time"
    )


# --------------------------------
# Prediction
# --------------------------------

if st.button("🚀 Predict delivery time"):

    # Create input dataframe
    input_data = pd.DataFrame({
        "distance": [distance],
        "Weatherconditions": [weather],
        "Road_traffic_density": [traffic],
        "Type_of_vehicle": [vehicle],
        "Festival": [festival],
        "City": [city],
        "Time_Orderd": [order_time.strftime("%H:%M:%S")],
        "Time_Order_picked": [picked_time.strftime("%H:%M:%S")]
    })

    # --------------------------------
    # Extract time features
    # --------------------------------

    order_datetime = pd.to_datetime(
        input_data["Time_Orderd"],
        format="%H:%M:%S"
    )

    picked_datetime = pd.to_datetime(
        input_data["Time_Order_picked"],
        format="%H:%M:%S"
    )

    input_data["order_hour"] = order_datetime.dt.hour
    input_data["order_minute"] = order_datetime.dt.minute

    input_data["picked_hour"] = picked_datetime.dt.hour
    input_data["picked_minute"] = picked_datetime.dt.minute

    # --------------------------------
    # Create time_category
    # --------------------------------

    hour = input_data["order_hour"].iloc[0]

    if 6 <= hour < 12:
        time_category = "Morning"
    elif 12 <= hour < 17:
        time_category = "Afternoon"
    elif 17 <= hour < 22:
        time_category = "Evening"
    else:
        time_category = "Night"

    input_data["time_category"] = time_category

    # --------------------------------
    # Remove original time columns
    # --------------------------------

    input_data = input_data.drop(
        columns=["Time_Orderd", "Time_Order_picked"]
    )

    # --------------------------------
    # One-hot encoding
    # --------------------------------

    input_encoded = pd.get_dummies(
        input_data,
        columns=[
            "Weatherconditions",
            "Road_traffic_density",
            "Type_of_vehicle",
            "Festival",
            "City",
            "time_category"
        ],
        drop_first=True,
        dtype=int
    )

    # --------------------------------
    # Make columns identical to training
    # --------------------------------

    input_encoded = input_encoded.reindex(
        columns=feature_columns,
        fill_value=0
    )

    # --------------------------------
    # Prediction
    # --------------------------------

    prediction = model.predict(input_encoded)[0]

    st.success(
        f"Estimated delivery time: **{prediction:.0f} minutes**"
    )

