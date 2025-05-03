import ccxt
from flask import Flask, request, jsonify
import telebot

MEXC_API_KEY = 'mx0vgl25FDEAdQxYh5'
MEXC_API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'
TELEGRAM_TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

exchange = ccxt.mexc({
    'apiKey': MEXC_API_KEY,
    'secret': MEXC_API_SECRET,
    'options': {'defaultType': 'future'}
})

def get_balance():
    try:
        balance = exchange.fetch_balance()
        usdt_balance = balance['total'].get('USDT', 0)
        return f"💰 Saldo total (USDT): {usdt_balance}"
    except Exception as e:
        return f"❗ Erro ao obter saldo: {str(e)}"

@app.route(f"/{TELEGRAM_TOKEN}", methods=['POST'])
def webhook():
    update = request.get_json()

    if 'message' in update and 'text' in update['message']:
        chat_id = update['message']['chat']['id']
        text = update['message']['text']

        if text == '/start':
            bot.send_message(chat_id, "✅ Bot de futuros MEXC online e funcionando!")
        elif text == '/balance':
            balance_msg = get_balance()
            bot.send_message(chat_id, balance_msg)

    return jsonify({'ok': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
