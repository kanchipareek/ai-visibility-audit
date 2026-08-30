import json
from prompts import PROMPTS_TO_CATEGORY

FILES = {
    "gemini": "analysis_v2.json",
    "openai": "analysis_v2_openai.json",
    "perplexity": "analyzed_perplexity.json",
}

rows = []

# --- Gemini: nested mentions array ---
with open(FILES["gemini"]) as f:
    gemini_data = json.load(f)

for entry in gemini_data:
    prompt = entry["prompt"]
    category = PROMPTS_TO_CATEGORY.get(prompt, "uncategorized")
    for mention in entry.get("mentions", []):
        rows.append({
            "prompt": prompt,
            "category": category,
            "model": "gemini",
            "brand": mention.get("brand"),
            "sentiment": mention.get("sentiment"),
            "position": mention.get("position"),
            "citations": [],
        })

# --- OpenAI: already flat, one row per mention ---
with open(FILES["openai"]) as f:
    openai_data = json.load(f)

for entry in openai_data:
    prompt = entry["prompt"]
    category = PROMPTS_TO_CATEGORY.get(prompt, "uncategorized")
    rows.append({
        "prompt": prompt,
        "category": category,
        "model": "openai",
        "brand": entry.get("brand"),
        "sentiment": entry.get("sentiment"),
        "position": entry.get("position"),
        "citations": [],
    })

# --- Perplexity: already flat, has citations instead of position ---
with open(FILES["perplexity"]) as f:
    perplexity_data = json.load(f)

for entry in perplexity_data:
    prompt = entry["prompt"]
    category = PROMPTS_TO_CATEGORY.get(prompt, "uncategorized")
    rows.append({
        "prompt": prompt,
        "category": category,
        "model": "perplexity",
        "brand": entry.get("brand"),
        "sentiment": entry.get("sentiment"),
        "position": None,
        "citations": entry.get("citations", []),
    })

with open("combined_results.json", "w") as f:
    json.dump(rows, f, indent=2)

print(f"Done. Combined {len(rows)} rows into combined_results.json")