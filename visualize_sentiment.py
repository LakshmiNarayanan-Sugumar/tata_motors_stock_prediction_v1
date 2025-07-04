import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load sentiment results
df = pd.read_csv('sentiment_results.csv')

# Plot sentiment distribution for Titles
plt.figure(figsize=(8, 6))
sns.countplot(x='Title Sentiment', data=df, palette='viridis')
plt.title('Title Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

# Plot sentiment distribution for Descriptions
plt.figure(figsize=(8, 6))
sns.countplot(x='Description Sentiment', data=df, palette='mako')
plt.title('Description Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()

# Optional: Plot sentiment over time if Published At is available
if 'published at' in df.columns:
    df['published at'] = pd.to_datetime(df['published at'])
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='published at', y='Title Sentiment', data=df, label='Title Sentiment')
    sns.lineplot(x='published at', y='Description Sentiment', data=df, label='Description Sentiment')
    plt.title('Sentiment Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sentiment')
    plt.legend()
    plt.savefig('sentiment_plot.png')
    plt.show()

    plt.show(block=True)

