import os
import hmac
import hashlib
import time
import requests
from flask import Flask, request

app = Flask(__name__)

API_KEY = 'mx0vgl25FDEAdQxYh5'
API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'
TELEGRAM_TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'
BASE_URL = 'https://api.mexc.com'

@app.route('/')
def index():
    return '✅ Bot rodando.'

def send_telegram(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    payload = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, json=payload)

def get_balance():
    path = '/api/v2/private/account/assets'
    url = BASE_URL + path
    timestamp = str(int(time.time() * 1000))
    query = f'timestamp={timestamp}'
    signature = hmac.new(API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': API_KEY
    }
    params = {'timestamp': timestamp, 'signature': signature}
    response = requests.get(url, headers=headers, params=params)
    try:
        data = response.json()
        for asset in data['data']: 
            if asset['currency'] == 'USDT':
                return asset['availableBalance']
        return 'USDT não encontrado'
    except Exception as e:
        return f'Erro: {e}'

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    update = request.get_json()
    if 'message' in update and 'text' in update['message']:
        text = update['message']['text']
        if text == '/start':
            send_telegram('✅ Bot de futuros MEXC online e funcionando!')
        elif text == '/status':
            send_telegram('✅ Status: Bot ativo. Conectado à MEXC.')
        elif text == '/balance':
            balance = get_balance()
            send_telegram(f'💰 Saldo disponível (USDT): {balance}')
        else:
            send_telegram('Comando não reconhecido.')
    return '', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
