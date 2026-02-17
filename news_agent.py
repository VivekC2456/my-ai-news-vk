import os
import requests
import json
import google.generativeai as genai

# Setup Keys from GitHub Secrets
genai.configure(api_key=os.environ["AI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 1. Fetch News
news_url = f"https://gnews.io{os.environ['NEWS_API_KEY']}"
data = requests.get(news_url).json()
articles = data.get('articles', [])[:5]

# 2. AI Summarize
feed = []
for art in articles:
    prompt = f"Rewrite this news for an Instagram story. Use 2 short punchy sentences and 1 emoji. Title: {art['title']}. Description: {art['description']}"
    summary = model.generate_content(prompt).text
    feed.append({"title": art['title'], "summary": summary, "url": art['url']})

# 3. Save for Web
os.makedirs('web', exist_ok=True)
with open('web/highlights.json', 'w') as f:
    json.dump(feed, f, indent=4)
