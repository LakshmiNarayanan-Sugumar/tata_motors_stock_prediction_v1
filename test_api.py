import requests

def test_api(api_key):
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)

    if response.status_code == 200:
        print("API Key is working! Here's a sample headline:")
        data = response.json()
        print(data['articles'][0]['title'])
    else:
        print(f"Error: {response.status_code}, {response.json()}")

api_key = '3111512a345945a0acdf47c8af27e10c'
test_api(api_key)
