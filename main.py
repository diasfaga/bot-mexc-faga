import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler
import asyncio

TOKEN = '8169013667:AAEyhMIOOXzLXu3hcslCiM_98Nza2Tn2zco'
CHAT_ID = '6237510676'
PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)

async def start(update: Update, context):
    await update.message.reply_text('✅ Bot de futuros MEXC online e funcionando!')

def setup_telegram_app():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    return application

telegram_app = setup_telegram_app()

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, telegram_app.bot)
    asyncio.run(telegram_app.process_update(update))
    return 'ok'

@app.route('/')
def index():
    return 'Bot rodando.'

if __name__ == '__main__':
    telegram_app.run_webhook(listen='0.0.0.0', port=PORT, url_path=TOKEN)
