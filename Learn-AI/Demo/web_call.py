from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GIMINI_OPENROUTER")

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    if request.method == "POST":
        user_prompt = request.form["prompt"]

        headers = {
            "Authorization": f"Bearer {api_key}",
            "HTTP-Referer": "http://localhost:5000",
            "X-Title": "Gemini Flask Demo"
        }

        payload = {
            "model": "google/gemini-2.0-flash-exp:free",
            "messages": [
                { "role": "user", "content": [ { "type": "text", "text": user_prompt } ] }
            ]
        }

        try:
            res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
            res.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
            data = res.json()
            response_text = data['choices'][0]['message']['content']
        except requests.exceptions.RequestException as e:
            response_text = f"❌ Request error: {e}"
        except Exception as e:
            response_text = f"❌ Unexpected error: {str(e)}"

    return render_template("index.html", response=response_text)

if __name__ == "__main__":
    app.run(debug=True)
