import pandas as pd

# Load the dataset
df = pd.read_csv("../KNBS_Villas_2010.csv")

# Quick overview
print(df.info())
print(df.describe())
print(df.head())
 
numeric_cols = [
    'month', 'year', 'number_units', 'number_beds', 'beds_occupied', 'beds_capacity',
    'units_occupied', 'units_capacity', 'total_revenue'
]

# Convert to numeric (coerce errors to NaN)
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with missing essential numeric data
df = df.dropna(subset=['month', 'total_revenue'])

df_cleaned = df.dropna(subset=['month', 'total_revenue'])

# Save cleaned data to CSV
df_cleaned.to_csv("C:\\Users\\Admin$\\Revenue_prediction\\KNBS_Villas_cleaned.csv", index=False)

print("Cleaned CSV file saved successfully!")

#Plot
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Add a small constant to avoid log(0)
df['log_revenue'] = np.log1p(df['total_revenue'])

# Boxplot
plt.figure(figsize=(10,6))
sns.boxplot(x='month', y='log_revenue', data=df)
plt.title("Distribution of log(Total Revenue + 1) by Month")
plt.xlabel("Month")
plt.ylabel("Log of Total Revenue")
plt.show()

# Scatter plot
plt.figure(figsize=(10,6))
sns.scatterplot(x='month', y='log_revenue', data=df, alpha=0.5)
sns.regplot(x='month', y='log_revenue', data=df, scatter=False, color='red')
plt.title("log(Total Revenue + 1) vs Month")
plt.xlabel("Month")
plt.ylabel("Log of Total Revenue")
plt.show()

#Standersise the data
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

# Example: standardize 'month', 'beds_occupied', 'beds_capacity', 'units_occupied', 'units_capacity'
features_to_scale = ['month', 'beds_occupied', 'beds_capacity', 'units_occupied', 'units_capacity']
df_scaled = df.copy()
df_scaled[features_to_scale] = scaler.fit_transform(df_scaled[features_to_scale])
print(df_scaled[features_to_scale].describe())
