import os
from openai import OpenAI
import json

# 🔑 STEP 1: Set your API key

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🔁 STEP 2: Load the first article from your raw file
with open("raw_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

article = articles[0]  # You can later loop this to generate more

# 🧠 STEP 3: Build a prompt to summarize and generate metadata
prompt = f"""
You are helping create a metadata file for a news microsite.
Please read the article details below and produce a JSON object in the following format:

{{
  "title": "...",
  "summary": "...",
  "timeline": ["...", "...", "..."],
  "why_matters": "...",
  "sources": [
    {{ "label": "...", "url": "..." }}
  ],
  "keywords": ["...", "..."]
}}

Only return valid JSON with no explanations.

---

Article:
Title: {article['title']}
Published At: {article['publishedAt']}
Source: {article['source']['name']}
URL: {article['url']}
Content: {article.get('content', '')}
"""

# 🧠 STEP 4: Call OpenAI to get the metadata
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.5
)

reply = response.choices[0].message.content.strip()

# Remove markdown-style code block fencing if present
if reply.startswith("```json"):
    reply = reply[7:]  # Remove ```json
if reply.endswith("```"):
    reply = reply[:-3]  # Remove trailing ```

# 💾 STEP 5: Parse and save metadata
try:
    metadata = json.loads(reply)

    # Ensure the public directory exists
    os.makedirs("public", exist_ok=True)

    with open("public/metadata.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)
    print("✅ metadata.json created.")
except json.JSONDecodeError:
    print("❌ Error parsing response. Here's what came back:\n")
    print(reply)
