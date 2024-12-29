from flask import Flask, request, render_template, jsonify
import requests
import json

app = Flask(__name__)


# Define the endpoint for the chatbot interface
@app.route("/")
def index():
    return render_template("chat.html")


# Endpoint to handle chat requests
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"error": "Message is required"}), 400

    # Proxy the request to the Ollama API
    try:
        with requests.post(
                'http://ollama:11434/api/chat',
                json={
                    "model": "llama2",
                    "messages": [
                        {"role": "user", "content": user_message}
                    ],
                    "stream": True
                },
                stream=True
        ) as response:
            response.raise_for_status()
            messages = []
            for chunk in response.iter_lines(decode_unicode=True):
                if chunk:  # Avoid blank lines
                    data = json.loads(chunk)
                    messages.append(data['message']['content'])

            return jsonify({"response": "".join(messages)})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
