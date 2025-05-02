import time
import hashlib
import hmac
import requests
from flask import Flask, request

app = Flask(__name__)

MEXC_API_KEY = 'mx0vgl25FDEAdQxYh5'
MEXC_API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'
TELEGRAM_TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'

BASE_URL = 'https://api.mexc.com'
BALANCE_ENDPOINT = '/api/v1/private/account/get-balance'  # confirme este endpoint no painel da MEXC


def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)


def get_futures_balance():
    timestamp = str(int(time.time() * 1000))
    params = f"timestamp={timestamp}"
    signature = hmac.new(MEXC_API_SECRET.encode(), params.encode(), hashlib.sha256).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'ApiKey': MEXC_API_KEY
    }

    url = f"{BASE_URL}{BALANCE_ENDPOINT}?{params}&signature={signature}"

    try:
        response = requests.get(url, headers=headers)
        data = response.json()

        if response.status_code == 200 and 'data' in data:
            usdt_balance = next((item['availableBalance'] for item in data['data'] if item['currency'] == 'USDT'), None)
            if usdt_balance is not None:
                return f"💰 Saldo disponível (USDT): {usdt_balance}"
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

    return {'ok': True}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
