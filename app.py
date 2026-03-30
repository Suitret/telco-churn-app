import streamlit as st
import pandas as pd
import numpy as np
import pickle

# Load saved objects
model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
columns = pickle.load(open("columns.pkl", "rb"))

st.set_page_config(page_title="Telco Churn Predictor")

st.title("📡 Telecom Customer Churn Prediction")
st.write("Predict whether a customer will churn and take action.")

# --- USER INPUTS ---
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0, 70.0)
total_charges = st.number_input("Total Charges", 0.0, 10000.0, 1000.0)

contract = st.selectbox("Contract Type", ["Month-to-month", "One year", "Two year"])
internet = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

# --- CREATE INPUT DATAFRAME ---
input_dict = {
    "tenure": tenure,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges,
}

input_df = pd.DataFrame([input_dict])

# --- One-hot encoding manually ---
for col in columns:
    if col not in input_df.columns:
        input_df[col] = 0

# Handle categorical manually
if contract == "One year":
    input_df["Contract_One year"] = 1
elif contract == "Two year":
    input_df["Contract_Two year"] = 1

if internet == "Fiber optic":
    input_df["InternetService_Fiber optic"] = 1
elif internet == "No":
    input_df["InternetService_No"] = 1

# Ensure correct column order
input_df = input_df[columns]

# Scale
input_scaled = scaler.transform(input_df)

# --- PREDICTION ---
if st.button("Predict Churn"):
    prediction = model.predict(input_scaled)[0]
    prob = model.predict_proba(input_scaled)[0][1]

    st.subheader("📊 Prediction Result")

    if prediction == 1:
        st.error(f"⚠️ Customer likely to churn ({prob:.2%})")
    else:
        st.success(f"✅ Customer likely to stay ({1 - prob:.2%})")

    # --- BUSINESS INSIGHT ---
    st.subheader("💡 Recommendation")

    if prob > 0.7:
        st.write("👉 Offer discount or promotion immediately.")
    elif prob > 0.4:
        st.write("👉 Engage customer with loyalty program.")
    else:
        st.write("👉 Customer is stable. Maintain service quality.")

