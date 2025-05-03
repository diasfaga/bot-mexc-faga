import ccxt
from flask import Flask, request
import requests

MEXC_API_KEY = 'mx0vgl25FDEAdQxYh5'
MEXC_API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'
TELEGRAM_TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'

app = Flask(__name__)
exchange = ccxt.mexc({
    'apiKey': MEXC_API_KEY,
    'secret': MEXC_API_SECRET
})

@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
def webhook():
    update = request.get_json()
    if 'message' in update and 'text' in update['message']:
        text = update['message']['text']
        chat_id = update['message']['chat']['id']

        if text == '/start':
            send_message(chat_id, "✅ Bot de futuros MEXC online e funcionando!")
        elif text == '/balance':
            try:
                balance = exchange.fetch_balance()
                usdt_balance = balance['total'].get('USDT', 'Indisponível')
                send_message(chat_id, f"💰 Saldo total (USDT): {usdt_balance}")
            except Exception as e:
                send_message(chat_id, f"❗ Erro ao obter saldo: {str(e)}")

    return {'ok': True}

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(url, json=payload)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
