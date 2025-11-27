# ======================================
# KNBS Revenue Prediction (User Input)
# ======================================

import pandas as pd
import numpy as np
from joblib import load
import os

# ------------------------
# 1. Paths to saved model and scaler
# ------------------------
output_dir = r"C:\Users\Admin$\Documents\KNBS_Project\outputs"
model_path = os.path.join(output_dir, "best_model.joblib")
scaler_path = os.path.join(output_dir, "scaler.joblib")

# ------------------------
# 2. Load model and scaler
# ------------------------
best_model = load(model_path)
scaler = load(scaler_path)

print("\n==============================")
print(" KNBS Revenue Prediction Tool ")
print("==============================\n")

# ------------------------
# 3. Get USER INPUT
# ------------------------

# Month
while True:
    try:
        month = int(input("Enter month (1–12): "))
        if 1 <= month <= 12:
            break
        else:
            print("❗ Month must be between 1 and 12.")
    except ValueError:
        print("❗ Please enter a valid number.")

# Beds occupied
while True:
    try:
        beds_occupied = float(input("Enter beds available: "))
        if beds_occupied >= 0:
            break
        else:
            print("❗ Beds occupied cannot be negative.")
    except ValueError:
        print("❗ Enter a valid numeric value.")

# Beds capacity
while True:
    try:
        beds_capacity = 20
        if beds_capacity > 0:
            break
        else:
            print("❗ Beds capacity must be greater than zero.")
    except ValueError:
        print("❗ Enter a valid numeric value.")


# ------------------------
# 4. Create DataFrame from input
# ------------------------
new_data = pd.DataFrame({
    'month': [month],
    'beds_occupied': [beds_occupied],
    'beds_capacity': [beds_capacity]
})

# ------------------------
# 5. Feature engineering
# ------------------------
new_data['occupancy_rate'] = new_data['beds_occupied'] / new_data['beds_capacity']
new_data['month_sin'] = np.sin(2 * np.pi * new_data['month'] / 12)
new_data['month_cos'] = np.cos(2 * np.pi * new_data['month'] / 12)

features = ['month_sin', 'month_cos', 'occupancy_rate']
X_new = new_data[features]

# ------------------------
# 6. Standardize features
# ------------------------
X_new_scaled = scaler.transform(X_new)

# ------------------------
# 7. Predict
# ------------------------
log_revenue_pred = best_model.predict(X_new_scaled)
revenue_pred = np.expm1(log_revenue_pred)  # convert back from log scale

# ------------------------
# 8. Display result
# ------------------------
print("\n--------------------------------------")
print(f" Predicted Revenue: KES {revenue_pred[0]:,.2f}")
print("--------------------------------------\n")
