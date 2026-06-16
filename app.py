import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()
POE_TOKEN = os.getenv("POE_SESSION_TOKEN")
if not POE_TOKEN:
    print("Warning: POE_SESSION_TOKEN not set. Add it to a .env file or environment.")

app = Flask(__name__, static_folder="static", template_folder="templates")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

POE_BASE = "https://poe.com"

def poe_headers():
    # Poe uses a session cookie for authentication. This example sets the cookie name that
    # commonly appears in browser requests. Your environment or Poe may differ.
    cookie = f"__Secure-next-auth.session-token={POE_TOKEN}" if POE_TOKEN else ""
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Cookie": cookie,
        # Optional: referer, origin
        "Referer": "https://poe.com/",
        "Origin": "https://poe.com",
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/bots")
def bots():
    """List available bots via a simple GraphQL query proxy.
    If this query doesn't work for you, consult the repo README and adjust the query.
    """
    query = "query GetBots { bots { id name description } }"
    payload = {"query": query}
    try:
        r = requests.post(f"{POE_BASE}/api/gql_POST", headers=poe_headers(), json=payload, timeout=15)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat", methods=["POST"])
def chat():
    """Send a message to Poe. Expects JSON: { "bot": "BOT_ID_OR_NAME", "text": "your message" }
    This proxies a GraphQL SendMessage mutation to Poe's public frontend endpoints.
    """
    data = request.get_json() or {}
    bot = data.get("bot")
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "No text provided"}), 400
    # Basic GraphQL mutation used by Poe's frontend. You may need to adjust fields/variables.
    graphql = (
        "mutation SendMessage($input: SendMessageInput!) {"
        " sendMessage(input: $input) { id text }"
        "}"
    )
    variables = {
        "input": {
            "bot": bot or "GPT-4",
            "text": text,
            # add other fields as needed: chatId, contextId, source, etc.
        }
    }
    payload = {"query": graphql, "variables": variables}
    try:
        r = requests.post(f"{POE_BASE}/api/gql_POST", headers=poe_headers(), json=payload, timeout=30)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8000)), debug=True)
