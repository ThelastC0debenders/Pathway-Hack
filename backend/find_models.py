import os
from google import genai

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("🔍 Querying available models for your API key...")

try:
    # We iterate through the models and check 'supported_actions'
    for model in client.models.list():
        # Action 'generateContent' is what we need for the Agent
        if hasattr(model, 'supported_actions') and "generateContent" in model.supported_actions:
            # We want the clean ID for the client (e.g., gemini-1.5-flash)
            # The .name property usually looks like 'models/gemini-1.5-flash'
            print(f"✅ Found: {model.name}")
except Exception as e:
    print(f"❌ Error: {e}")