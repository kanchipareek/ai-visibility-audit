import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

with open("results_openai.json") as f:
    data = json.load(f)

# Build one big prompt covering all entries at once (single API call)
entries_text = ""
for i, entry in enumerate(data):
    entries_text += f"\n--- Entry {i} ---\nPrompt: {entry['prompt']}\nResponse: {entry['response']}\n"

batch_prompt = f"""You are analyzing {len(data)} AI responses about helpdesk software brands.

For EACH entry below, identify:
- Which of these brands are mentioned: Zendesk, Freshdesk, Intercom, Gorgias, Help Scout, Kustomer
- The sentiment toward each mentioned brand (positive/neutral/negative)
- The position (1st, 2nd, 3rd... mentioned in that response)

Return ONLY a JSON array, one object per entry, in this exact format, nothing else, no markdown fences:
[
  {{"entry_index": 0, "mentions": [{{"brand": "Zendesk", "sentiment": "positive", "position": 1}}]}},
  ...
]

If no brand is mentioned in an entry, use "mentions": [].

{entries_text}
"""

model = genai.GenerativeModel("gemini-3.6-flash")
response = model.generate_content(batch_prompt)

raw = response.text.strip()
raw = re.sub(r"^```json|```$", "", raw, flags=re.MULTILINE).strip()
parsed = json.loads(raw)

analyzed = []
for item in parsed:
    entry = data[item["entry_index"]]
    for mention in item["mentions"]:
        analyzed.append({
            "prompt": entry["prompt"],
            "model_name": entry.get("model_name", "openai"),
            "brand": mention["brand"],
            "sentiment": mention["sentiment"],
            "position": mention["position"],
        })

with open("analysis_v2_openai.json", "w") as f:
    json.dump(analyzed, f, indent=2)

print(f"Done. Saved {len(analyzed)} entries.")