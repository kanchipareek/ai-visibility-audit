import os
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
    test_prompts = prompts[:3]

    for p in test_prompts:
        print(f"PROMPT: {p}")
        print(f"RESPONSE: {ask_gemini(p)}")
        print("-" * 41)


