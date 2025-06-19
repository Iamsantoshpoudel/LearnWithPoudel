from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
import requests
import markdown

load_dotenv()
api_key = os.getenv("GIMINI_OPENROUTER")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")  # Just serve the page

@app.route("/generate", methods=["POST"])
def generate():
    try:
        user_prompt = request.form.get("prompt", "")
        if not user_prompt:
            return jsonify({ "error": "Empty prompt." }), 400

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

        res = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
        res.raise_for_status()

        raw_text = res.json()['choices'][0]['message']['content']
        html_response = markdown.markdown(raw_text)

        return jsonify({ "response_html": html_response })

    except Exception as e:
        return jsonify({ "error": str(e) }), 500
if __name__ == "__main__":
    app.run(debug=True)
