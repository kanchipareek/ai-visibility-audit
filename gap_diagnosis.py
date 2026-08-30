import json
from collections import defaultdict

BRANDS = ["Zendesk", "Freshdesk", "Intercom", "Gorgias", "Help Scout", "Kustomer"]

def main():
    with open("combined_results.json") as f:
        rows = json.load(f)

    by_prompt_model = defaultdict(list)
    for row in rows:
        key = (row["prompt"], row["model"])
        by_prompt_model[key].append(row)

    gap_report = defaultdict(list)

    for (prompt, model), entries in by_prompt_model.items():
        mentioned_brands = {e["brand"] for e in entries if e["brand"]}
        category = entries[0]["category"]

        for target_brand in BRANDS:
            if target_brand in mentioned_brands:
                continue

            competitors_here = [
                {"brand": e["brand"], "sentiment": e["sentiment"], "citations": e["citations"]}
                for e in entries if e["brand"] and e["brand"] != target_brand
            ]

            if competitors_here:
                gap_report[target_brand].append({
                    "prompt": prompt,
                    "model": model,
                    "category": category,
                    "lost_to": competitors_here,
                })

    with open("gap_diagnosis.json", "w") as f:
        json.dump(gap_report, f, indent=2)

    for brand, losses in gap_report.items():
        print(f"{brand}: lost {len(losses)} prompts to competitors")

if __name__ == "__main__":
    main()