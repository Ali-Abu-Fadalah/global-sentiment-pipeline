import os
import requests
import feedparser
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import time
from datetime import datetime, timezone

# 1. Load Environment Variables
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

HF_API_TOKEN = os.getenv("HF_API_TOKEN")
HF_MODEL_ID = os.getenv("HF_MODEL_ID")

ALERT_THRESHOLD = float(os.getenv("ALERT_THRESHOLD", "0.80"))
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# 2. Database Connection Setup
def get_mongo_collection():
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    db = client[DB_NAME]
    return db[COLLECTION_NAME]

# 3. Fetch Public News Feed (RSS)
def fetch_news(feed_url="https://finance.yahoo.com/news/rss"):
    print(f"Fetching news from {feed_url}...")
    feed = feedparser.parse(feed_url)
    articles = []
    # Limit to top 5 recent articles for demonstration
    for entry in feed.entries[:5]: 
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if hasattr(entry, 'published') else None
        })
    return articles

# 4. Sentiment Classification via Hugging Face Serverless API
def analyze_sentiment(text):
    print(f"Analyzing sentiment for: '{text[:50]}...'")
    api_url = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL_ID}"
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"}
    payload = {"inputs": text}
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        
        # Free Inference API might need time to load the model into memory
        if response.status_code == 503:
            print("Model is loading, waiting 15 seconds...")
            time.sleep(15)
            response = requests.post(api_url, headers=headers, json=payload)
            
        if response.status_code != 200:
            print(f"Error from HF API: {response.text}")
            return None
            
        result = response.json()
        
        # Result format typically: [[{'label': 'POSITIVE', 'score': 0.99}, {'label': 'NEGATIVE', 'score': 0.01}]]
        # We extract the one with the highest confidence score
        best_score = max(result[0], key=lambda x: x['score'])
        return best_score
        
    except Exception as e:
        print(f"Failed to analyze sentiment: {e}")
        return None

# 5. Logging and Alerting
def send_discord_alert(title, sentiment_label, sentiment_score):
    if DISCORD_WEBHOOK_URL and DISCORD_WEBHOOK_URL != "placeholder":
        print(f"Sending Discord alert for high {sentiment_label} sentiment...")
        data = {
            "content": f"🚨 **High Confidence Sentiment Alert** 🚨\n**Article:** {title}\n**Sentiment:** {sentiment_label} ({sentiment_score:.2f})"
        }
        try:
            requests.post(DISCORD_WEBHOOK_URL, json=data)
        except Exception as e:
            print(f"Failed to send Discord alert: {e}")

# 6. Main Pipeline Execution
def main():
    try:
        collection = get_mongo_collection()
    except Exception as e:
        print(f"Failed to connect to MongoDB: {e}")
        return

    articles = fetch_news()
    
    for article in articles:
        sentiment = analyze_sentiment(article['title'])
        if sentiment:
            log_entry = {
                "article_title": article['title'],
                "article_link": article['link'],
                "published_at": article['published'],
                "sentiment_label": sentiment['label'],
                "sentiment_score": sentiment['score'],
                "processed_at": datetime.now(timezone.utc)
            }
            
            # Save structured logs directly to MongoDB Atlas
            try:
                collection.insert_one(log_entry)
                print(f"Saved to MongoDB: {sentiment['label']} ({sentiment['score']:.2f})")
            except Exception as e:
                print(f"Failed to save to MongoDB: {e}")
            
            # Check Alert Threshold (e.g., alert if confidence is very high)
            if sentiment['score'] >= ALERT_THRESHOLD:
                send_discord_alert(article['title'], sentiment['label'], sentiment['score'])
                
        # Slight delay to respect API rate limits
        time.sleep(1)

if __name__ == "__main__":
    main()

