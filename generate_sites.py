import os
import json
import shutil
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Load all articles
with open("raw_articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

# Create base folder for output
output_base = "public"
os.makedirs(output_base, exist_ok=True)

for idx, article in enumerate(articles):
    public_dir = os.path.join(output_base, f"site-{idx+1}")
    os.makedirs(public_dir, exist_ok=True)

    # Copy public assets
    shutil.copy("styles.css", os.path.join(public_dir, "styles.css"))
    shutil.copy("script.js", os.path.join(public_dir, "script.js"))

    # Build GPT prompt
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

    # Query OpenAI
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    reply = response.choices[0].message.content.strip()

    # Strip code block markers if present
    if reply.startswith("```json"):
        reply = reply[7:]
    if reply.endswith("```"):
        reply = reply[:-3]

    try:
        metadata = json.loads(reply)

        # Save metadata.json
        with open(os.path.join(public_dir, "metadata.json"), "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

        # Generate public index.html
        index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{metadata['title']}</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <main>
    <h1>{metadata['title']}</h1>
    <p class="summary">{metadata['summary']}</p>

    <section>
      <h2>Timeline</h2>
      <ul>
        {''.join(f"<li>{item}</li>" for item in metadata['timeline'])}
      </ul>
    </section>

    <section>
      <h2>Why It Matters</h2>
      <p>{metadata['why_matters']}</p>
    </section>

    <footer>
      <h3>Sources</h3>
      <ul>
        {''.join(f'<li><a href="{src["url"]}" target="_blank">{src["label"]}</a></li>' for src in metadata['sources'])}
      </ul>
    </footer>
  </main>
</body>
</html>"""

        with open(os.path.join(public_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(index_html)

        print(f"✅ Created microsite for article {idx+1}")

    except json.JSONDecodeError:
        print(f"❌ JSON parse error in site-{idx+1}. GPT reply was:\n{reply}")
