import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np

# Load the sentiment data
df = pd.read_csv('sentiment_results.csv')

# Extract sentiment data
text_data = ' '.join(df['Title Sentiment'].astype(str) + ' ' + df['Description Sentiment'].astype(str))

# Calculate sentiment percentages
sentiment_counts = Counter(text_data.split())
total_sentiments = sum(sentiment_counts.values())

positive_percent = (sentiment_counts.get('Positive', 0) / total_sentiments) * 100
negative_percent = (sentiment_counts.get('Negative', 0) / total_sentiments) * 100
neutral_percent = (sentiment_counts.get('Neutral', 0) / total_sentiments) * 100

# Define a color function for sentiment words
def sentiment_color(word, **kwargs):
    if word == 'Positive':
        return 'green'
    elif word == 'Negative':
        return 'red'
    elif word == 'Neutral':
        return 'gray'
    return 'blue'

# Generate the Word Cloud
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    color_func=sentiment_color,
    font_path='/System/Library/Fonts/Supplemental/Arial.ttf'  # Adjust based on your system
).generate(text_data)

# Plot the Word Cloud
plt.figure(figsize=(12, 8))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title(f"Word Cloud for Tata Motors Sentiments\nPositive: {positive_percent:.2f}%, Negative: {negative_percent:.2f}%, Neutral: {neutral_percent:.2f}%")
plt.savefig("ordcloud.png")
plt.show()
