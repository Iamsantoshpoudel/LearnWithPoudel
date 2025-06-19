from dotenv import load_dotenv
import os
import requests
from rich.console import Console

# Load environment variables from .env
load_dotenv()


OPENROUTER_API_KEY = os.getenv('GIMINI_OPENROUTER')

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "  ",  # Optional
    "X-Title": "   "       # Optional
}


user_prompt = input(f"\nEnter your prompt:\n")

payload = {
    "model": "google/gemini-2.0-flash-exp:free",
    "messages": [
        {
            "role": "user",
            "content": [
                { "type": "text", "text": user_prompt },
                # {
                #     "type": "image_url",
                #     "image_url": {
                #         "url": "#"
                #     }
                # }
            ]
        }
    ]
}
console = Console()
with console.status("[bold green]Thinking..."):
       response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
       content = response.json()['choices'][0]['message']['content']

# Print the result
print("\n 🤔Response :\n")
print(content)
