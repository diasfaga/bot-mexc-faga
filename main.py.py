import os
from flask import Flask, request
import telegram

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
PORT = int(os.environ.get('PORT', 5000))

bot = telegram.Bot(token=TOKEN)
app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    text = update.message.text

    if text == "/start":
        bot.sendMessage(chat_id=chat_id, text="Bot de futuros MEXC online e funcionando!")
    else:
        bot.sendMessage(chat_id=chat_id, text=f"Você disse: {text}")

    return 'ok'

@app.route('/')
def index():
    return 'Bot rodando.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT)