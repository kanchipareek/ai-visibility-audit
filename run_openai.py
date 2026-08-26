import json
import time
from dotenv import load_dotenv
import os
from openai import OpenAI
from prompts import prompts
from datetime import datetime,timezone

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

results = []

for i, prompt in enumerate(prompts):
    print(f"running prompt {i+1}/{len(prompts)}: {prompt[:50]}...")
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",
            messages=[{"role": "user", "content": prompt}],
        )
        answer = response.choices[0].message.content
        results.append({"prompt" : prompt, "response": answer, "model": "gpt-5-nano", "timestamp": datetime.now(timezone.utc).isoformat()})
    except Exception as e:
        print(f"failed on prompt {i+1}: {e}")
        results.append({"prompt" : prompt, "response": None, "error": str(e), "model": "gpt-5-nano", "timestamp": datetime.now(timezone.utc).isoformat()})
    time.sleep(1)  

with open("results_openai.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Done. Saved {len(results)} results to results_openai.json ")
