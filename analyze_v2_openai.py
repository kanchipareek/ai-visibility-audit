import os
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

BRANDS = ["Zendesk", "Intercom", "Kustomer", "Help Scout", "Gorgias", "Freshdesk"]


def classify_response(prompt, response_text):
    if not response_text:
        return {"mentions": []}

    classifier_prompt = f"""You are analyzing an AI chatbot's response to a buyer's question about helpdesk software.

Buyer's question: "{prompt}"

AI's response: "{response_text}"

Brands to check for: {", ".join(BRANDS)}

For each brand that is mentioned in the AI's response, determine:
- Whether it was actually recommended, mentioned neutrally, or mentioned negatively (e.g. "I don't recommend X" counts as negative)
- Roughly what position it appeared in the response (1st brand mentioned, 2nd, etc.)

Return ONLY valid JSON, no other text, in this exact format:
{{
  "mentions": [
    {{"brand": "BrandName", "sentiment": "positive|neutral|negative", "position": 1}}
  ]
}}

If no brands are mentioned, return {{"mentions": []}}."""

    result = model.generate_content(classifier_prompt)
    text = result.text.strip()

    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"mentions": [], "parse_error": text}


if __name__ == "__main__":
    with open("results_openai.json", "r") as f:
        results = json.load(f)

    analyzed = []

    for i, entry in enumerate(results):
        print(f"[{i+1}/{len(results)}] classifying: {entry['prompt'][:50]}...")
        classification = classify_response(entry["prompt"], entry["response"])

        analyzed.append({
            "prompt": entry["prompt"],
            "model": entry["model"],
            "timestamp": entry["timestamp"],
            "mentions": classification.get("mentions", [])
        })

        time.sleep(2)

    with open("analysis_v2_openai.json", "w") as f:
        json.dump(analyzed, f, indent=2)

    print(f"\nDone. Saved {len(analyzed)} classified results to analysis_v2_openai.json\n")

    for brand in BRANDS:
        brand_mentions = [
            m for a in analyzed for m in a["mentions"] if m["brand"] == brand
        ]
        count = len(brand_mentions)
        positive = sum(1 for m in brand_mentions if m["sentiment"] == "positive")
        print(f"{brand}: {count} mentions ({positive} positive)")