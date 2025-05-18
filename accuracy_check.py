import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load your data
df = pd.read_csv('data.csv')

# Drop rows where Actual Price is missing (NaN)
df = df.dropna(subset=['Actual Price'])

# Calculate metrics
mae = mean_absolute_error(df['Actual Price'], df['Predicted Price'])
mse = mean_squared_error(df['Actual Price'], df['Predicted Price'])
rmse = mse ** 0.5
mape = (abs((df['Actual Price'] - df['Predicted Price']) / df['Actual Price'])).mean() * 100

print(f"Mean Absolute Error (MAE): {mae:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")