# ======================================
# KNBS Revenue Analysis: Regression Models
# ======================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, SGDRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# ------------------------
# 1. Load the dataset
# ------------------------
df = pd.read_csv("C:\\Users\\Admin$\\Documents\\KNBS_Project\\KNBS_Villas_cleaned.csv")

# Optional: log-transform revenue to handle skewness
df['log_revenue'] = np.log1p(df['total_revenue'])

# Feature engineering: occupancy rate
df['occupancy_rate'] = df['beds_occupied'] / df['beds_capacity']

# Cyclical encoding for month
df['month_sin'] = np.sin(2 * np.pi * df['month']/12)
df['month_cos'] = np.cos(2 * np.pi * df['month']/12)

# ------------------------
# 2. Select features & target
# ------------------------
features = ['month_sin', 'month_cos', 'occupancy_rate']
X = df[features].fillna(0)
y = df['log_revenue'].fillna(0)

# ------------------------
# 3. Train-test split
# ------------------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ------------------------
# 4. Standardize features
# ------------------------
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# ======================================
# 5a. Linear Regression (normal)
# ======================================
lr = LinearRegression()
lr.fit(X_train_scaled, y_train)
y_pred_lr = lr.predict(X_test_scaled)
print("Linear Regression R2:", r2_score(y_test, y_pred_lr))
print("Linear Regression MSE:", mean_squared_error(y_test, y_pred_lr))

# ======================================
# 5b. Decision Tree Regressor
# ======================================
dt = DecisionTreeRegressor(max_depth=5, random_state=42)
dt.fit(X_train_scaled, y_train)
y_pred_dt = dt.predict(X_test_scaled)
print("Decision Tree R2:", r2_score(y_test, y_pred_dt))
print("Decision Tree MSE:", mean_squared_error(y_test, y_pred_dt))

# ======================================
# 5c. Random Forest Regressor
# ======================================
rf = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
rf.fit(X_train_scaled, y_train)
y_pred_rf = rf.predict(X_test_scaled)
print("Random Forest R2:", r2_score(y_test, y_pred_rf))
print("Random Forest MSE:", mean_squared_error(y_test, y_pred_rf))

# ======================================
# 6. Linear Regression with Gradient Descent
# ======================================
sgd = SGDRegressor(max_iter=1000, learning_rate='invscaling', eta0=0.01, random_state=42)
train_loss = []
test_loss = []

# Manual loop to record loss
for epoch in range(100):
    sgd.partial_fit(X_train_scaled, y_train)
    y_train_pred = sgd.predict(X_train_scaled)
    y_test_pred = sgd.predict(X_test_scaled)
    train_loss.append(mean_squared_error(y_train, y_train_pred))
    test_loss.append(mean_squared_error(y_test, y_test_pred))

print("SGD Regressor R2 (test):", r2_score(y_test, sgd.predict(X_test_scaled)))

# Plot loss curve
plt.figure(figsize=(10,6))
plt.plot(train_loss, label='Train Loss')
plt.plot(test_loss, label='Test Loss')
plt.xlabel("Epoch")
plt.ylabel("MSE Loss")
plt.title("Gradient Descent Loss Curve")
plt.legend()
plt.show()

# ======================================
# 7. Scatter Plot Before and After (Linear Regression)
# ======================================
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred_lr, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Actual log Revenue")
plt.ylabel("Predicted log Revenue")
plt.title("Linear Regression: Actual vs Predicted")
plt.show()

from joblib import dump

# 1. Collect R2 scores
r2_scores = {
    'LinearRegression': r2_score(y_test, y_pred_lr),
    'DecisionTree': r2_score(y_test, y_pred_dt),
    'RandomForest': r2_score(y_test, y_pred_rf),
    'SGDRegressor': r2_score(y_test, sgd.predict(X_test_scaled))
}

# 2. Find best model
best_model_name = max(r2_scores, key=r2_scores.get)
print("Best model:", best_model_name, "R2:", r2_scores[best_model_name])

# 3. Map names to objects
models = {
    'LinearRegression': lr,
    'DecisionTree': dt,
    'RandomForest': rf,
    'SGDRegressor': sgd
}

best_model = models[best_model_name]

# 4. Save the best model
dump(best_model, "C:\\Users\\Admin$\\Documents\\KNBS_Project\\best_model.joblib")
dump(scaler, "C:\\Users\\Admin$\\Documents\\KNBS_Project\\scaler.joblib")  # save scaler too
print(f"{best_model_name} saved successfully!")
