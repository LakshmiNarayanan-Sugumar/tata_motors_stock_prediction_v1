import requests
import csv

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

# Replace with your API key
api_key = '3111512a345945a0acdf47c8af27e10c'
fetch_tata_motors_news(api_key)

