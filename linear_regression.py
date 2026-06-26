import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# Load sentiment and stock data
sentiment_data = pd.read_csv('sentiment_results.csv')
stock_data = pd.read_csv('cleaned_tata_motors_stock_data.csv')

# Convert date columns to datetime
sentiment_data['Published At'] = pd.to_datetime(sentiment_data['Published At'])
stock_data['Date'] = pd.to_datetime(stock_data['Date'], utc=True)

# Merge data on closest date
merged_data = pd.merge_asof(
    sentiment_data.sort_values('Published At'),
    stock_data.sort_values('Date'),
    left_on='Published At',
    right_on='Date',
    direction='backward'
)

# Add lagged close price (yesterday's close) — no leakage
merged_data['Close_lag1'] = merged_data['Close'].shift(1)

# Drop first row (no lag available) and any missing values
merged_data = merged_data.dropna(subset=[
    'Title Sentiment', 'Description Sentiment', 'Close', 'Close_lag1'
])

if merged_data.empty:
    raise ValueError("All data removed after dropping missing values.")

# Label encode sentiment columns
label_encoder = LabelEncoder()
merged_data['Title Sentiment'] = label_encoder.fit_transform(
    merged_data['Title Sentiment']
)
merged_data['Description Sentiment'] = label_encoder.fit_transform(
    merged_data['Description Sentiment']
)

print("Sentiment columns encoded successfully.")

# Features and target — no same-day High/Low
X = merged_data[['Title Sentiment', 'Description Sentiment', 'Close_lag1']]
y = merged_data['Close']
dates = merged_data['Date']

# ── TIME-BASED SPLIT (no shuffle) ─────────────────────────────────────────────
split = int(len(X) * 0.80)
X_train, X_test = X.iloc[:split], X.iloc[split:]
y_train, y_test = y.iloc[:split], y.iloc[split:]
dates_test = dates.iloc[split:]

print(f"Train samples: {len(X_train)}")
print(f"Test samples:  {len(X_test)}")

# Train Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Evaluate
mae  = mean_absolute_error(y_test, y_pred)
mse  = mean_squared_error(y_test, y_pred)
r2   = r2_score(y_test, y_pred)

print(f"\nMAE:  {mae:.4f}")
print(f"MSE:  {mse:.4f}")
print(f"R²:   {r2:.4f}")

if r2 > 0.75:
    print("The model has a high predictive accuracy.")
elif r2 > 0.5:
    print("The model has moderate predictive accuracy.")
else:
    print("The model has low predictive accuracy.")

# Model Coefficients
coefficients = pd.DataFrame({
    'Feature': X.columns,
    'Coefficient': model.coef_
})
print("\nModel Coefficients:")
print(coefficients)

# ── PLOT: Actual vs Predicted ──────────────────────────────────────────────────
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red')
plt.xlabel('Actual Close Prices')
plt.ylabel('Predicted Close Prices')
plt.title('Actual vs Predicted Stock Prices (Fixed — No Leakage)')
plt.savefig('actual_vs_predicted.png', bbox_inches='tight')
plt.show()

# ── PLOT: Residual ─────────────────────────────────────────────────────────────
plt.figure(figsize=(10, 6))
sns.residplot(x=y_test, y=y_pred, color='blue')
plt.axhline(y=0, color='red', linestyle='--')
plt.xlabel('Actual Close Prices')
plt.ylabel('Residuals (Actual - Predicted)')
plt.title('Residual Plot (Fixed — No Leakage)')
plt.savefig('residual_plot.png', bbox_inches='tight')
plt.show()

# ── SAVE RESULTS ──────────────────────────────────────────────────────────────
results_df = pd.DataFrame({
    'Date': dates_test.values,
    'Actual': y_test.values,
    'Predicted': y_pred
})
results_df.to_csv('prediction_results.csv', index=False)
print("\nResults saved to prediction_results.csv")

# ── FUTURE PREDICTION ─────────────────────────────────────────────────────────
latest_sentiment = sentiment_data.iloc[-1]
latest_close = stock_data.iloc[-1]['Close']

future_data = pd.DataFrame({
    'Title Sentiment': [label_encoder.transform(
        [latest_sentiment['Title Sentiment']])[0]],
    'Description Sentiment': [label_encoder.transform(
        [latest_sentiment['Description Sentiment']])[0]],
    'Close_lag1': [latest_close]
})

future_prediction = model.predict(future_data)
future_date = stock_data.iloc[-1]['Date'] + pd.Timedelta(days=1)
print(f"\nPredicted Close Price for {future_date}: ₹{future_prediction[0]:.2f}")
print("\nDone!")