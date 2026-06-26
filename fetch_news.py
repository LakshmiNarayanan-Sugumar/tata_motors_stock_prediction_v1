import requests
import csv
import os

def fetch_tata_motors_news(api_key):
    query = "Tata Motors"
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        articles = response.json().get('articles', [])
        print(f"Found {len(articles)} articles.")
        
        # Save data to CSV
        with open('tata_motors_news.csv', mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Title", "Description", "URL", "Published At", "Source"])

            for article in articles:
                writer.writerow([
                    article.get('title', 'N/A'),
                    article.get('description', 'N/A'),
                    article.get('url', 'N/A'),
                    article.get('publishedAt', 'N/A'),
                    article.get('source', {}).get('name', 'N/A')
                ])
                
        print("Data saved to 'tata_motors_news.csv' successfully!")
    else:
        print(f"Error: {response.status_code}, {response.json()}")

# Load API key from environment variable
api_key = os.environ.get("NEWS_API_KEY", "your_api_key_here")
fetch_tata_motors_news(api_key)