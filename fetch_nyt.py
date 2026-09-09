import os
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("NYT_API_KEY")
TOPIC = "artificial intelligence"  # Set your keyword/topic filter
OUTPUT_FILE = "nyt_articles.json"

# Define the historical years you want to query for today's month and day
YEARS_TO_CHECK = [2020, 2015, 2010, 2005, 2000, 1990, 1980]

def fetch_this_day_in_history():
    if not API_KEY:
        raise ValueError("Missing NYT_API_KEY environment variable.")

    today = datetime.utcnow()
    month_str = today.strftime("%m")
    day_str = today.strftime("%d")

    fetched_articles = []

    for year in YEARS_TO_CHECK:
        # Construct YYYYMMDD for this day in history
        target_date = f"{year}{month_str}{day_str}"
        print(f"Fetching articles for {target_date}...")

        url = "https://api.nytimes.com/svc/search/v2/articlesearch.json"
        params = {
            'q': TOPIC,
            'begin_date': target_date,
            'end_date': target_date,
            'api-key': API_KEY
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                docs = response.json().get('response', {}).get('docs', [])
                for doc in docs:
                    fetched_articles.append({
                        'historical_year': year,
                        'headline': doc['headline']['main'],
                        'snippet': doc.get('snippet', ''),
                        'pub_date': doc.get('pub_date'),
                        'url': doc.get('web_url'),
                        'section': doc.get('section_name', '')
                    })
            else:
                print(f"Warning: HTTP {response.status_code} for date {target_date}")
        except Exception as e:
            print(f"Error fetching for date {target_date}: {e}")

    # Overwrite JSON file with today's historical query results
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(fetched_articles, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved {len(fetched_articles)} historical articles to {OUTPUT_FILE}.")

if __name__ == "__main__":
    fetch_this_day_in_history()
