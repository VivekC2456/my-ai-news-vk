import os
import google.generativeai as genai
import requests
import json
from datetime import datetime

# Configure API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

if not GNEWS_API_KEY:
    print("Error: GNEWS_API_KEY not set in environment")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)

# Build news URL with API key
news_url = f"https://gnews.io/api/v4/search?q=AI&token={GNEWS_API_KEY}"

def fetch_news_with_retry(url, max_retries=3, timeout=10):
    """Fetch news with retry logic and timeout"""
    for attempt in range(max_retries):
        try:
            print(f"Fetching news (attempt {attempt + 1}/{max_retries})...")
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            print(f"Request timeout (attempt {attempt + 1}/{max_retries})")
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error (attempt {attempt + 1}/{max_retries}): {str(e)[:100]}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None
        except ValueError as e:
            print(f"Invalid JSON response: {e}")
            return None
        
        if attempt < max_retries - 1:
            import time
            wait_time = 2 ** attempt
            print(f"Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
    
    print("Failed to fetch news after all retries")
    return None

try:
    data = fetch_news_with_retry(news_url)
    
    if data is None or not data.get('articles'):
        print("No articles retrieved. Exiting gracefully.")
        exit(0)
    
    # Process articles
    articles = data.get('articles', [])[:5]  # Get top 5
    
    print(f"\nFetched {len(articles)} articles at {datetime.now()}")
    
    for article in articles:
        print(f"- {article.get('title', 'No title')}")
    
    # Add your Gemini processing here    
    
except Exception as e:
    print(f"Fatal error: {type(e).__name__}: {e}")
    exit(1)
