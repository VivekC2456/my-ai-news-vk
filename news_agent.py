import os
import requests
import json
import google.generativeai as genai
from datetime import datetime

# 1. Configuration - uses standard keys from GitHub Secrets
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

if not GNEWS_API_KEY or not GOOGLE_API_KEY:
    print("Error: API Keys not set.")
    exit(1)

# Initialize Gemini
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# GNews URL (using 'apikey' which is the standard parameter)
news_url = f"https://gnews.io{GNEWS_API_KEY}"

def run_agent():
    try:
        print("Fetching latest news...")
        response = requests.get(news_url, timeout=15)
        response.raise_for_status()
        articles = response.json().get('articles', [])
        
        if not articles:
            print("No news found.")
            return

        highlights = []
        for art in articles:
            print(f"Summarizing: {art['title']}")
            
            # AI Prompt for Instagram-style highlights
            prompt = f"Summarize this news in 2 punchy sentences + 1 emoji for a mobile feed: {art['title']}. {art['description']}"
            ai_response = model.generate_content(prompt)
            
            highlights.append({
                "title": art['title'],
                "summary": ai_response.text if ai_response.text else "Brief summary unavailable.",
                "url": art['url']
            })

        # CRITICAL STEP: Create the web folder and save the JSON
        os.makedirs('web', exist_ok=True)
        with open('web/highlights.json', 'w') as f:
            json.dump(highlights, f, indent=4)
        
        print(f"Done! Created web/highlights.json with {len(highlights)} articles.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_agent()
