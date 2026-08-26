import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-3.6-flash")
prompt="what's the best helpdesk software right now"
response = model.generate_content(prompt)
print(response.text)


