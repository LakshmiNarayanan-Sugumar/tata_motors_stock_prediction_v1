import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load sentiment and stock data
sentiment_data = pd.read_csv('sentiment_results.csv')
stock_data = pd.read_csv('cleaned_tata_motors_stock_data.csv')

# Convert date columns to datetime for accurate merging
sentiment_data['Published At'] = pd.to_datetime(sentiment_data['Published At'], utc=True)
stock_data['Date'] = pd.to_datetime(stock_data['Date'], utc=True)

# Merge data on the closest date using 'Published At'
merged_data = pd.merge_asof(sentiment_data.sort_values('Published At'),
                              stock_data.sort_values('Date'),
                              left_on='Published At',
                              right_on='Date',
                              direction='backward')

# Convert categorical sentiment values to numerical values
sentiment_mapping = {'Negative': -1, 'Neutral': 0, 'Positive': 1}
merged_data['Title Sentiment'] = merged_data['Title Sentiment'].map(sentiment_mapping)
merged_data['Description Sentiment'] = merged_data['Description Sentiment'].map(sentiment_mapping)

# Check for any remaining missing values
print('Missing values before cleaning:')
print(merged_data[['Title Sentiment', 'Description Sentiment', 'Close', 'High', 'Low']].isnull().sum())

# Drop rows with missing values
merged_data = merged_data.dropna(subset=['Title Sentiment', 'Description Sentiment', 'Close', 'High', 'Low'])

if merged_data.empty:
    raise ValueError("All data removed after dropping missing values. Check your input data.")

# Plot correlation heatmap
plt.figure(figsize=(10, 8))
corr_matrix = merged_data[['Title Sentiment', 'Description Sentiment', 'Close', 'High', 'Low']].corr()
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Sentiment vs. Stock Price Correlation Heatmap - Tata Motors')
plt.show()

# Plot scatter plots
plt.figure(figsize=(10, 6))
sns.scatterplot(x='Title Sentiment', y='Close', data=merged_data)
plt.title('Title Sentiment vs Stock Close Price')
plt.xlabel('Title Sentiment')
plt.ylabel('Stock Close Price')
plt.show()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='Description Sentiment', y='Close', data=merged_data)
plt.title('Description Sentiment vs Stock Close Price')
plt.xlabel('Description Sentiment')
plt.ylabel('Stock Close Price')
plt.show()
