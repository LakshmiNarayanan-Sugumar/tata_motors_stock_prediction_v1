import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder

# Load sentiment and stock data
sentiment_data = pd.read_csv('sentiment_results.csv')
stock_data = pd.read_csv('cleaned_tata_motors_stock_data.csv')

# Convert date columns to datetime for accurate merging
sentiment_data['Published At'] = pd.to_datetime(sentiment_data['Published At'])
stock_data['Date'] = pd.to_datetime(stock_data['Date'], utc=True)

# Merge data on the closest date using 'published_at'
merged_data = pd.merge_asof(sentiment_data.sort_values('Published At'),
                              stock_data.sort_values('Date'),
                              left_on='Published At',
                              right_on='Date',
                              direction='backward')

# Check for missing values
print('Missing values before cleaning:')
print(merged_data[['Title Sentiment', 'Description Sentiment', 'Close', 'High', 'Low']].isnull().sum())

# Drop rows with missing values
merged_data = merged_data.dropna(subset=['Title Sentiment', 'Description Sentiment', 'Close', 'High', 'Low'])

if merged_data.empty:
    raise ValueError("All data removed after dropping missing values. Check your input data.")

# Perform Label Encoding for sentiment columns
label_encoder = LabelEncoder()
merged_data['Title Sentiment'] = label_encoder.fit_transform(merged_data['Title Sentiment'])
merged_data['Description Sentiment'] = label_encoder.fit_transform(merged_data['Description Sentiment'])

print("Sentiment columns encoded successfully.")

# Select features and target variable
X = merged_data[['Title Sentiment', 'Description Sentiment', 'High', 'Low']]
y = merged_data['Close']

# Save corresponding dates for the predictions
dates = merged_data['Date']

# Split data into train and test sets
X_train, X_test, y_train, y_test, dates_train, dates_test = train_test_split(X, y, dates, test_size=0.2, random_state=42)

# Train the Linear Regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict using the model
y_pred = model.predict(X_test)

# Evaluate model performance
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"Mean Absolute Error (MAE): {mae}")
print(f"Mean Squared Error: {mse}")
print(f"R^2 Score: {r2}")

# Visualize predictions vs actual values
plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.xlabel('Actual Close Prices')
plt.ylabel('Predicted Close Prices')
plt.title('Actual vs Predicted Stock Prices')
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='red')
plt.show()

# Residual Plot for Error Analysis
plt.figure(figsize=(10, 6))
sns.residplot(x=y_test, y=y_pred, color='blue')
plt.xlabel('Actual Close Prices')
plt.ylabel('Residuals (Actual - Predicted)')
plt.title('Residual Plot')
plt.axhline(y=0, color='red', linestyle='--')
plt.show()

# Conclusion based on R2 Score
if r2 > 0.75:
    print("The model has a high predictive accuracy. The features explain a significant portion of the variance.")
elif r2 > 0.5:
    print("The model has moderate predictive accuracy. Some patterns are captured, but improvements can be made.")
else:
    print("The model has low predictive accuracy. Consider adding more features or trying different algorithms.")

# Display Model Coefficients
coefficients = pd.DataFrame({'Feature': X.columns, 'Coefficient': model.coef_})
print("Model Coefficients:")
print(coefficients)

# Save model results to CSV
results_df = pd.DataFrame({'Date': dates_test, 'Actual': y_test, 'Predicted': y_pred})
results_df.to_csv('prediction_results.csv', index=False)
print("Results saved to prediction_results.csv")

# Future Price Prediction
latest_sentiment = sentiment_data.iloc[-1]
latest_stock = stock_data.iloc[-1]

future_data = pd.DataFrame({
    'Title Sentiment': [label_encoder.transform([latest_sentiment['Title Sentiment']])[0]],
    'Description Sentiment': [label_encoder.transform([latest_sentiment['Description Sentiment']])[0]],
    'High': [latest_stock['High']],
    'Low': [latest_stock['Low']]
})

future_prediction = model.predict(future_data)
future_date = latest_stock['Date'] + pd.Timedelta(days=1)  # Assuming next trading day
print(f"Predicted Close Price for {future_date}: {future_prediction[0]}")
