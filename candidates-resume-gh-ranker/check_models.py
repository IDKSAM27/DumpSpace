import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_AI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GOOGLE_AI_API_KEY or GOOGLE_AI_API_KEY == "YOUR_GOOGLE_AI_API_KEY":
    print("Error: Please paste your GOOGLE_AI_API_KEY into the script.")
else:
    try:
        genai.configure(api_key=GOOGLE_AI_API_KEY)
        
        print("Fetching available models for your API key...")
        print("="*30)
        
        # List all models that support 'generateContent'
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model Name: {m.name}")
                print(f"Description: {m.description}\n")

        print("="*30)
        print("\n--- End of List ---")
        print("\nACTION: Copy one of the 'Model Name' values above (e.g., 'models/gemini-1.0-pro')")
        print("and use it to replace 'gemini-pro' in your rank_candidates.py script.")

    except Exception as e:
        print(f"An error occurred while trying to list models: {e}")
        print("Please double-check your API key and internet connection.")