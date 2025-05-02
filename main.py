import os
import time
import hmac
import hashlib
import requests
from flask import Flask, request

TOKEN = "7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8"
CHAT_ID = "6237510676"
API_KEY = "mx0vgl25FDEAdQxYh5"
API_SECRET = "54ace640205a4dc2a8188b4e58132ca6"
BASE_URL = "https://api.mexc.com"

app = Flask(__name__)

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, json=payload)

def get_account_balance():
    path = "/api/v1/private/account/asset"
    timestamp = str(int(time.time() * 1000))
    signature_payload = f"api_key={API_KEY}&req_time={timestamp}"
    signature = hmac.new(API_SECRET.encode(), signature_payload.encode(), hashlib.sha256).hexdigest()
    headers = {"Content-Type": "application/json"}
    params = {
        "api_key": API_KEY,
        "req_time": timestamp,
        "sign": signature
    }
    url = f"{BASE_URL}{path}"
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for asset in data.get("data", []):
            if asset["currency"] == "USDT":
                return asset["availableBalance"]
    return "Erro"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data:
        text = data["message"].get("text", "")
        chat_id = data["message"]["chat"]["id"]
        if text == "/start":
            send_telegram_message("✅ Bot de futuros MEXC online e funcionando!")
        elif text == "/status":
            send_telegram_message("✅ Status: Bot ativo. Conectado à MEXC.")
        elif text == "/balance":
            balance = get_account_balance()
            send_telegram_message(f"💰 Saldo disponível (USDT): {balance}")
        else:
            send_telegram_message("Comando não reconhecido.")
    return {"ok": True}

@app.route("/", methods=["GET"])
def home():
    return "✅ Bot rodando."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
