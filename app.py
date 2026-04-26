from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

@app.route("/interpret", methods=["POST"])
def interpret():
    data = request.get_json()
    dream_text = data.get("dream", "")
    if not dream_text:
        return jsonify({"error": "没有梦境内容"}), 400

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "你是梦缇斯，一个温暖的心理学陪伴者。你的回答要像老朋友一样真诚、具体、有画面感。不要分点，不要用'综上所述'。请复述用户梦境的细节，并给出一个极小、可操作的动作建议。"},
            {"role": "user", "content": dream_text}
        ],
        "max_tokens": 800,
        "temperature": 0.85
    }
    try:
        resp = requests.post(DEEPSEEK_URL, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        ai_response = resp.json()["choices"][0]["message"]["content"]
        return jsonify({"result": ai_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)