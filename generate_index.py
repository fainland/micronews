import os
import json

SITES_DIR = "sites"
OUTPUT_FILE = "index.html"

# Start building the HTML
html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Live News Microsites</title>
  <style>
    body {
      font-family: sans-serif;
      background: #f4f4f4;
      padding: 2rem;
      max-width: 800px;
      margin: auto;
    }
    .site {
      background: white;
      padding: 1rem 1.5rem;
      border-radius: 8px;
      margin-bottom: 1.5rem;
      box-shadow: 0 0 10px rgba(0,0,0,0.05);
    }
    .site a {
      text-decoration: none;
      color: #c0392b;
      font-weight: bold;
    }
    .site p {
      color: #333;
    }
  </style>
</head>
<body>
  <h1>📰 Latest Auto-Generated News Summaries</h1>
"""

# Scan each microsite
for folder in sorted(os.listdir(SITES_DIR)):
    site_path = os.path.join(SITES_DIR, folder)
    metadata_path = os.path.join(site_path, "static", "metadata.json")

    if os.path.isdir(site_path) and os.path.isfile(metadata_path):
        try:
            with open(metadata_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            title = data.get("title", "Untitled")
            summary = data.get("summary", "")
            html += f"""
  <div class="site">
    <a href="{folder}/index.html" target="_blank">{title}</a>
    <p>{summary}</p>
  </div>
"""
        except Exception as e:
            print(f"⚠️ Could not read metadata for {folder}: {e}")

# Close HTML
html += """
</body>
</html>
"""

# Write to file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

print("✅ index.html generated successfully.")
