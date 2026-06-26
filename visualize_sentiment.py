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
plt.savefig('title_sentiment_distribution.png', bbox_inches='tight')  # ← correct
plt.show()

# Plot sentiment distribution for Descriptions
plt.figure(figsize=(8, 6))
sns.countplot(x='Description Sentiment', data=df, palette='mako')
plt.title('Description Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.savefig('description_sentiment_distribution.png', bbox_inches='tight')  # ← correct
plt.show()