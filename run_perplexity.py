import os, json, time, requests
from dotenv import load_dotenv
from prompts import prompts

load_dotenv()
API_KEY = os.environ["PERPLEXITY_API_KEY"]
URL = "https://api.perplexity.ai/chat/completions"

def call_perplexity(prompt, model="sonar-pro"):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    payload = {"model": model, "messages": [{"role": "user", "content": prompt}]}
    r = requests.post(URL, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return {
        "prompt": prompt,
        "response": data["choices"][0]["message"]["content"],
        "citations": data.get("citations", []),
        "model": model,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
    }

if __name__ == "__main__":
    results = []
    for p in prompts:
        print(f"Running: {p[:50]}...")
        results.append(call_perplexity(p))
        time.sleep(1)
    with open("results_perplexity.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDone. Saved {len(results)} raw responses to results_perplexity.json\n")