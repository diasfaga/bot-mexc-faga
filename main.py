import time
import hmac
import hashlib
import requests
import json
from flask import Flask, request

app = Flask(__name__)

# Configurações do bot
TELEGRAM_TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'
MEXC_API_KEY = 'mx0vgl25FDEAdQxYh5'
MEXC_API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'

# Função para enviar mensagem ao Telegram
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

# Função para obter saldo de futuros na MEXC
def get_futures_balance():
    url = 'https://api.mexc.com/api/v1/private/account/assets'
    timestamp = int(time.time() * 1000)
    query = f'timestamp={timestamp}'
    signature = hmac.new(MEXC_API_SECRET.encode(), query.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        'Content-Type': 'application/json',
        'ApiKey': MEXC_API_KEY
    }
    params = {
        'timestamp': timestamp,
        'signature': signature
    }

    response = requests.get(url, headers=headers, params=params)
    print("Resposta bruta da MEXC:", response.text)  # <-- Aqui vamos capturar o que vem

    if response.status_code == 200:
        data = response.json()
        if 'data' in data:
            for asset in data['data']:
                if asset['currency'] == 'USDT':
                    available_balance = asset['availableBalance']
                    return f'Saldo disponível (USDT): {available_balance}'
            return 'USDT não encontrado.'
        else:
            return f"Erro: {data}"
    else:
        return f"Erro HTTP: {response.status_code}"

@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def telegram_webhook():
    update = request.get_json()
    if 'message' in update and 'text' in update['message']:
        text = update['message']['text']
        if text == '/start':
            send_telegram_message('✅ Bot de futuros MEXC online e funcionando!')
        elif text == '/status':
            send_telegram_message('✅ Status: Bot ativo. Conectado à MEXC.')
        elif text == '/balance':
            balance = get_futures_balance()
            send_telegram_message(f'💰 {balance}')
        else:
            send_telegram_message('Comando não reconhecido.')
    return 'ok'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
