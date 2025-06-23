import os
import requests
import json
import difflib


API_KEY = os.getenv("NEWS_API_KEY")

url = 'https://newsapi.org/v2/top-headlines'
params = {
    'language': 'en',
    'pageSize': 10,
    'apiKey': API_KEY
}


response = requests.get(url, params=params)
articles = response.json().get('articles', [])

filtered = []
titles_seen = []

def is_similar(title1, title2, threshold=0.85):
    return difflib.SequenceMatcher(None, title1, title2).ratio() >= threshold

for article in articles:
    title = article.get("title", "").strip()

    # Check similarity to existing titles
    if not any(is_similar(title, seen) for seen in titles_seen):
        filtered.append(article)
        titles_seen.append(title)

with open("raw_articles.json", "w", encoding="utf-8") as f:
    json.dump(filtered, f, indent=2)

print(f"✅ Fetched {len(filtered)} unique articles.")
