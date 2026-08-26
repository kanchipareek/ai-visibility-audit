import os
import json
import time
from datetime import datetime, timezone
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import prompts

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")


def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    results = []

    for i, p in enumerate(prompts):
        print(f"[{i+1}/{len(prompts)}] {p}")
        try:
            answer = ask_gemini(p)
        except Exception as e:
            print(f"Error for prompt '{p}': {e}")
            answer = None

        results.append({
            "prompt": p,
            "response": answer,
            "model": "gemini-3.6-flash",
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

        time.sleep(2)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"Done. Saved {len(results)} results to results.json")