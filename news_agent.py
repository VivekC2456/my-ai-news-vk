import os
import google.generativeai as genai
import requests
import json
from datetime import datetime

# 1. Setup Keys (Check names carefully!)
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY")

if not GNEWS_API_KEY or not GOOGLE_API_KEY:
    print("Error: API Keys not found in environment.")
    exit(1)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Fetch News (Using 'apikey' as the correct parameter)
news_url = f"https://gnews.io{GNEWS_API_KEY}"

def run_agent():
    try:
        print("Fetching news articles...")
        response = requests.get(news_url, timeout=10)
        response.raise_for_status()
        data = response.json()
        articles = data.get('articles', [])
        
        if not articles:
            print("No articles found.")
            return

        highlights = []
        for art in articles:
            print(f"Summarizing: {art['title']}")
            
            # Use Gemini to summarize
            prompt = f"Summarize this news in 2 short sentences with 1 emoji for an Instagram story: {art['title']}. {art['description']}"
            ai_response = model.generate_content(prompt)
            summary = ai_response.text if ai_response.text else "No summary available."
            
            highlights.append({
                "title": art['title'],
                "summary": summary,
                "url": art['url']
            })

        # 3. Save the file where the website can find it
        os.makedirs('web', exist_ok=True)
        with open('web/highlights.json', 'w') as f:
            json.dump(highlights, f, indent=4)
        
        print(f"Successfully saved {len(highlights)} highlights to web/highlights.json")

    except Exception as e:
        print(f"Agent Error: {e}")

if __name__ == "__main__":
    run_agent()
