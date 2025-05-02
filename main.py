import os
import requests
from flask import Flask, request

TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'
MEXC_API_KEY = 'mx0vgl25FDEAdQxYh5'
MEXC_API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'

app = Flask(__name__)

@app.route('/')
def index():
    return '✅ Bot rodando e pronto.'

@app.route(f'/7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8', methods=['POST'])
def webhook():
    data = request.get_json()
    print('📥 Recebido do Telegram:', data)
    if 'message' in data and 'text' in data['message']:
        chat_id = data['message']['chat']['id']
        text = data['message']['text']
        if text == '/start':
            send_message(chat_id, '✅ Bot de futuros MEXC online e funcionando!')
        elif text == '/help':
            send_message(chat_id, 'ℹ️ Comandos disponíveis: /start, /stop, /status, /help')
        elif text == '/status':
            send_message(chat_id, '✅ Status: Bot ativo. Conectado à MEXC.')
        elif text == '/balance':
            balance = get_balance()
            send_message(chat_id, f'💰 Saldo disponível: {balance} USDT')
    return 'ok'

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=payload)
    print('📤 Resposta enviada:', r.text)

def get_balance():
    url = 'https://api.mexc.com/api/v3/account'
    headers = {
        'X-MEXC-APIKEY': MEXC_API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        for asset in data.get('balances', []):
            if asset['asset'] == 'USDT':
                return asset['free']
        return '0'
    else:
        print('Erro ao buscar saldo:', response.text)
        return 'Erro'

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
