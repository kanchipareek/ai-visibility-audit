import json
BRANDS = ["Zendesk", "Intercom", "Kustomer", "Freshdesk", "Help Scout", "Gorgias"]

def find_mentions(text,brands):
    if not text:
        return []
    mentions = []
    lower_text = text.lower()
    for brand in brands:
        if brand.lower() in lower_text:
            position = lower_text.find(brand.lower())
            mentions.append({"brand": brand, "char_position": position})

    mentions.sort(key=lambda m: m["char_position"])
    return mentions

if __name__ == "__main__":
    with open("results.json", "r") as f:
        results = json.load(f)

    analyzed=[]

    for entry in results:
        mentions = find_mentions(entry["response"], BRANDS)
        analyzed.append({
            "prompt": entry["prompt"],
            "model": entry["model"],
            "timestamp": entry["timestamp"],
            "mentions": mentions,
            "mention_count": len(mentions)
        })

        with open("analyzed.json", "w") as f:
            json.dump(analyzed, f, indent=2)

            print(f"Analyzed {len(analyzed)} prompts.")

            for brand in BRANDS:
                count = sum(1 for a in analyzed if any(m["brand"] == brand for m in a["mentions"]))
                pct = round(count / len(analyzed) * 100, 1) 
                print(f"{brand}: mentioned in {count} /{len(analyzed)} prompts ({pct}%)" )
                
                