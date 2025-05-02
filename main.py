import os
import requests
from flask import Flask, request

TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'

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
    return 'ok'

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    r = requests.post(url, json=payload)
    print('📤 Resposta enviada:', r.text)

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
