import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the cleaned data
df = pd.read_csv('cleaned_tata_motors_news.csv')

# Initialize the Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

def get_sentiment(text):
    if pd.isnull(text):
        return 'Neutral'
    
    scores = analyzer.polarity_scores(text)
    compound_score = scores['compound']
    
    if compound_score >= 0.05:
        return 'Positive'
    elif compound_score <= -0.05:
        return 'Negative'
    else:
        return 'Neutral'

# Perform sentiment analysis on the Title and Description
df['Title Sentiment'] = df['Title'].apply(get_sentiment)
df['Description Sentiment'] = df['Description'].apply(get_sentiment)

# Save results to a new CSV
df.to_csv('sentiment_results.csv', index=False)

print("Sentiment analysis completed. Results saved to sentiment_results.csv")
