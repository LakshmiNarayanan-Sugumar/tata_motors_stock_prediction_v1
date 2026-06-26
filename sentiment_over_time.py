import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
df = pd.read_csv('sentiment_results.csv')

# Convert 'Published At' to datetime
df['Published At'] = pd.to_datetime(df['Published At'])

# Map sentiment to numeric values
sentiment_mapping = {'Positive': 1, 'Neutral': 0, 'Negative': -1}
df['description_sentiment_score'] = df['Description Sentiment'].map(sentiment_mapping)
df['title_sentiment_score'] = df['Title Sentiment'].map(sentiment_mapping)

# Group by date and calculate the average sentiment score for both
daily_description_sentiment = df.groupby(df['Published At'].dt.date)['description_sentiment_score'].mean().reset_index()
daily_title_sentiment = df.groupby(df['Published At'].dt.date)['title_sentiment_score'].mean().reset_index()

# Plot the sentiment over time
plt.figure(figsize=(12, 7))

sns.lineplot(x='Published At', y='description_sentiment_score', data=daily_description_sentiment, marker='o', label='Description Sentiment', color='blue')
sns.lineplot(x='Published At', y='title_sentiment_score', data=daily_title_sentiment, marker='s', label='Title Sentiment', color='red')

plt.title('Sentiment Over Time for Tata Motors')
plt.xlabel('Date')
plt.ylabel('Average Sentiment Score')
plt.legend()
plt.grid(True)
plt.savefig("sentiment_over_time.png")
plt.show()
