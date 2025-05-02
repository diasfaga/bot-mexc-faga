import ccxt
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

MEXC_API_KEY = 'mx0vgl25FDEAdQxYh5'
MEXC_API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'
TELEGRAM_TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'

# Configure ccxt para mexc futures
exchange = ccxt.mexc({
    'apiKey': MEXC_API_KEY,
    'secret': MEXC_API_SECRET,
    'options': {
        'defaultType': 'swap',  # importante: para futuros (swap)
    }
})

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

def get_futures_balance():
    try:
        balance = exchange.fetch_balance()
        usdt_balance = balance['total'].get('USDT', None)
        if usdt_balance is not None:
            return f"💰 Saldo disponível (USDT): {usdt_balance}"
        else:
            return "❗ USDT não encontrado no saldo."
    except Exception as e:
        return f"❗ Erro ao obter saldo: {str(e)}"

@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update and 'text' in update['message']:
        text = update['message']['text']

        if text == '/balance':
            balance_message = get_futures_balance()
            send_telegram_message(balance_message)
        elif text == '/start':
            send_telegram_message("✅ Bot de futuros MEXC online e funcionando!")

    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
