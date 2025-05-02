import os
import time
import hmac
import hashlib
import requests
from flask import Flask, request

app = Flask(__name__)

API_KEY = "mx0vgl25FDEAdQxYh5"
API_SECRET = "54ace640205a4dc2a8188b4e58132ca6"
BOT_TOKEN = "7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8"
CHAT_ID = "6237510676"

BASE_URL = "https://api.mexc.com"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text}
    requests.post(url, data=data)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    data = request.get_json()
    if "message" in data and "text" in data["message"]:
        text = data["message"]["text"]
        if text == "/start":
            send_telegram_message("✅ Bot de futuros MEXC online e funcionando!")
        elif text == "/status":
            send_telegram_message("✅ Status: Bot ativo. Conectado à MEXC.")
        elif text == "/balance":
            balance = get_account_balance()
            send_telegram_message(f"💰 Saldo disponível: {balance} USDT")
        else:
            send_telegram_message("❓ Comando não reconhecido.")
    return "ok"

def get_account_balance():
    path = "/api/v3/account"
    timestamp = str(int(time.time() * 1000))
    query_string = f"timestamp={timestamp}"
    signature = hmac.new(API_SECRET.encode(), query_string.encode(), hashlib.sha256).hexdigest()
    headers = {"X-MEXC-APIKEY": API_KEY}
    url = f"{BASE_URL}{path}?{query_string}&signature={signature}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for asset in data.get("balances", []):
            if asset["asset"] == "USDT":
                return asset["free"]
    return "Erro"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
