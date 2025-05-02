import os
from flask import Flask, request
import requests

TOKEN = '8169013667:AAEyhMIOOXzLXu3hcslCiM_98Nza2Tn2zco'
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

app = Flask(__name__)

@app.route('/')
def index():
    return '✅ Bot rodando.'

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json()
    chat_id = data['message']['chat']['id']
    text = data['message']['text']

    if text == '/start':
        send_message(chat_id, '✅ Bot de futuros MEXC online e funcionando!')
    else:
        send_message(chat_id, f'Você disse: {text}')

    return 'ok'

def send_message(chat_id, text):
    payload = {'chat_id': chat_id, 'text': text}
    requests.post(TELEGRAM_API_URL, json=payload)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
