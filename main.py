import time
import hashlib
import hmac
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

MEXC_API_KEY = 'mx0vgl25FDEAdQxYh5'
MEXC_API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'
TELEGRAM_TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'

BASE_URL = 'https://contract.mexc.com'
BALANCE_ENDPOINT = '/api/v1/private/account/assets'

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

def get_futures_balance():
    timestamp = str(int(time.time() * 1000))
    params = f'timestamp={timestamp}'
    signature = hmac.new(MEXC_API_SECRET.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'ApiKey': MEXC_API_KEY,
        'Request-Time': timestamp,
        'Signature': signature
    }

    url = f'{BASE_URL}{BALANCE_ENDPOINT}?{params}'

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if data.get('success') and 'data' in data:
            usdt_asset = next((item for item in data['data'] if item.get('currency') == 'USDT'), None)
            if usdt_asset:
                available_balance = usdt_asset.get('availableBalance')
                return f"💰 Saldo disponível (USDT): {available_balance}"
            else:
                return "❗ USDT não encontrado."
        else:
            return f"❗ Erro API: {data}"

    except Exception as e:
        return f"❗ Erro: {str(e)}"

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
