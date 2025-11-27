from fastapi import FastAPI
from pydantic import BaseModel, Field
from joblib import load
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# ------------------------------------
# Load Model & Scaler
# ------------------------------------
MODEL_PATH = r"C:\Users\Admin$\Documents\KNBS_Project\outputs\best_model.joblib"
SCALER_PATH = r"C:\Users\Admin$\Documents\KNBS_Project\outputs\scaler.joblib"

model = load(MODEL_PATH)
scaler = load(SCALER_PATH)

# ------------------------------------
# Create FastAPI App
# ------------------------------------
app = FastAPI(
    title="KNBS Revenue Prediction API",
    description="API that predicts hotel/lodge revenue using ML model",
    version="1.0.0"
)

# ------------------------------------
# Enable CORS (required for web apps)
# ------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this on deployment
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------
# Pydantic Input Model
# ------------------------------------
class PredictionInput(BaseModel):
    month: int = Field(..., ge=1, le=12, description="Month of the year (1-12)")
    beds_occupied: float = Field(..., ge=0, description="Occupancy")
    beds_capacity: float = 20
# ------------------------------------
# Prediction Route
# ------------------------------------
@app.post("/predict")
def predict(data: PredictionInput):

    # Convert to DataFrame
    df = pd.DataFrame([data.dict()])

    # Feature engineering
    df["occupancy_rate"] = df["beds_occupied"] / df["beds_capacity"]
    df["month_sin"] = np.sin(2 * np.pi * df["month"] / 12)
    df["month_cos"] = np.cos(2 * np.pi * df["month"] / 12)

    X = df[["month_sin", "month_cos", "occupancy_rate"]]

    # Scale features
    X_scaled = scaler.transform(X)

    # Predict log revenue
    log_pred = model.predict(X_scaled)

    # Reverse log1p → revenue
    revenue_pred = np.expm1(log_pred)[0]

    return {
        "predicted_revenue": float(revenue_pred),
        "message": "Prediction generated successfully"
    }

# ------------------------------------
# Root endpoint
# ------------------------------------
@app.get("/")
def home():
    return {"message": "KNBS Revenue Prediction API is running!"}
