
import os
import time
import threading
import requests
from flask import Flask, request

# Configurações
BOT_TOKEN = "8169013667:AAEyhMIOOXzLXu3hcslCiM_98Nza2Tn2zco"
CHAT_ID = None
app = Flask(__name__)

def enviar_telegram(msg):
    if CHAT_ID:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={"chat_id": CHAT_ID, "text": msg})

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    global CHAT_ID
    data = request.get_json()
    if "message" in data:
        CHAT_ID = data["message"]["chat"]["id"]
        texto = data["message"].get("text", "")
        if texto == "/start":
            enviar_telegram("✅ Bot iniciado com sucesso!")
            threading.Thread(target=sinal_teste).start()
        elif texto == "/status":
            enviar_telegram("📡 Bot ativo e monitorando.")
    return {"ok": True}

@app.route("/")
def home():
    return "Bot online e aguardando comandos."

def sinal_teste():
    time.sleep(5)
    enviar_telegram("🟢 Sinal de COMPRA simulado: ALTUSDT\nRSI: 28.5\nPreço: 0.035\nQtd: 50\n🎯 TP: 0.037\n🛑 SL: 0.031")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
