import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY or OPENAI_API_KEY == "YOUR_OPENAI_API_KEY":
    print("Error: Please paste your OPENAI_API_KEY into the .env file.")
else:
    try:
        openai.api_key = OPENAI_API_KEY
        
        print("Fetching available models for your API key...")
        print("="*30)
        
        # List all available models
        models = openai.Model.list()
        
        # Print each model's name and description
        for model in models['data']:
            print(f"Model ID: {model['id']}")
            print(f"Description: {model.get('description', 'No description available')}\n")

        print("="*30)
        print("\n--- End of List ---")
        print("\nACTION: Copy one of the 'Model ID' values above (e.g., 'gpt-4') and use it in your script.")

    except Exception as e:
        print(f"An error occurred while trying to list models: {e}")
        print("Please double-check your API key and internet connection.")
