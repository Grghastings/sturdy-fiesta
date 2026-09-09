import os
import json
import requests
from datetime import datetime, timedelta

# NYT API configuration
API_KEY = os.environ.get("NYT_API_KEY")
TOPIC = "artificial intelligence"  # Change to your topic
OUTPUT_FILE = "nyt_articles.json"

def fetch_daily_articles():
    if not API_KEY:
        raise ValueError("Missing NYT_API_KEY environment variable.")

    # Get yesterday's date (YYYYMMDD format) to ensure full day coverage
    target_date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y%m%m")
    
    url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
    params = {
        'q': TOPIC,
        'begin_date': target_date,
        'end_date': target_date,
        'api-key': API_KEY
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    
    docs = response.json().get('response', {}).get('docs', [])
    
    new_articles = []
    for doc in docs:
        new_articles.append({
            'headline': doc['headline']['main'],
            'snippet': doc.get('snippet', ''),
            'pub_date': doc.get('pub_date'),
            'url': doc.get('web_url'),
            'section': doc.get('section_name', '')
        })

    # Load existing articles if file exists
    existing_articles = []
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_articles = json.load(f)
        except json.JSONDecodeError:
            existing_articles = []

    # Merge avoiding duplicates based on URL
    existing_urls = {item['url'] for item in existing_articles}
    for art in new_articles:
        if art['url'] not in existing_urls:
            existing_articles.append(art)

    # Save back to JSON file
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(existing_articles, f, indent=2, ensure_ascii=False)

    print(f"Added {len(new_articles)} new articles for {target_date}.")

if __name__ == "__main__":
    fetch_daily_articles()
