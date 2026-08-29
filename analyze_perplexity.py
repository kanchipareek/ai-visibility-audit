import json
import re
import time
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")

BRANDS = ["Zendesk", "Intercom", "Kustomer", "Help Scout", "Gorgias", "Freshdesk"]


def get_all_brand_mentions(raw_results):
    combined_input = ""
    for i, entry in enumerate(raw_results):
        response_text = entry.get("response", "") or ""
        combined_input += f"\n---ENTRY {i}---\n{response_text}\n"

    batch_prompt = f"""You are analyzing {len(raw_results)} AI responses about helpdesk software.
Each entry is separated by ---ENTRY N--- markers.

Brands to check for: {", ".join(BRANDS)}

For each entry, identify which brands are mentioned, their sentiment (positive, neutral, negative),
and quote the exact sentence where each brand appears, so citation markers like [1] or [5] near it can be found later.

Return ONLY valid JSON, no markdown, no explanation. Format:
{{
  "0": [{{"brand": "Zendesk", "sentiment": "positive", "quote": "exact sentence here"}}],
  "1": [],
  "2": [{{"brand": "Freshdesk", "sentiment": "neutral", "quote": "exact sentence here"}}]
}}

If an entry mentions no brands, use an empty array for that index.

Entries:
{combined_input}
"""

    result = model.generate_content(batch_prompt)
    text = result.text.strip()
    text = re.sub(r"^```json|```$", "", text, flags=re.MULTILINE).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print("Judge returned invalid JSON. Raw output below:")
        print(text[:2000])
        return {}


def find_citations_for_brand(brand, full_response, citations_list):
    all_urls = set()

    for match in re.finditer(re.escape(brand), full_response, re.IGNORECASE):
        start = match.start()
        window_start = max(0, start - 50)
        window_end = min(len(full_response), start + len(brand) + 200)
        window = full_response[window_start:window_end]

        markers = re.findall(r"\[(\d+)\]", window)
        for m in markers:
            pos = int(m) - 1
            if 0 <= pos < len(citations_list):
                all_urls.add(citations_list[pos])

    return list(all_urls)

def main():
    with open("results_perplexity.json") as f:
        raw_results = json.load(f)

    print(f"Sending all {len(raw_results)} entries to Gemini in one batch call...")
    all_mentions = get_all_brand_mentions(raw_results)

    analyzed = []
    for i, entry in enumerate(raw_results):
        response_text = entry.get("response", "") or ""
        citations_list = entry.get("citations", [])
        mentions = all_mentions.get(str(i), [])

        brands_mentioned = []
        for m in mentions:
            urls = find_citations_for_brand(m["brand"], response_text, citations_list)
            brands_mentioned.append({
                "brand": m["brand"],
                "sentiment": m["sentiment"],
                "citations": urls
            })

        analyzed.append({
            "prompt": entry["prompt"],
            "brands_mentioned": brands_mentioned
        })

    with open("analyzed_perplexity.json", "w") as f:
        json.dump(analyzed, f, indent=2)

    print(f"Done. Saved {len(analyzed)} analyzed results to analyzed_perplexity.json")


if __name__ == "__main__":
    main()