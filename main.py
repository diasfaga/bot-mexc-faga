import ccxt
import telebot

MEXC_API_KEY = 'mx0vgl25FDEAdQxYh5'
MEXC_API_SECRET = '54ace640205a4dc2a8188b4e58132ca6'
TELEGRAM_TOKEN = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'
CHAT_ID = '6237510676'

bot = telebot.TeleBot(TELEGRAM_TOKEN)
exchange = ccxt.mexc({
    'apiKey': MEXC_API_KEY,
    'secret': MEXC_API_SECRET
})

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ Bot de futuros MEXC online e funcionando!")

@bot.message_handler(commands=['balance'])
def send_balance(message):
    try:
        balance = exchange.fetch_balance()
        usdt_balance = balance['total']['USDT']
        bot.reply_to(message, f"💰 Saldo total (USDT): {usdt_balance}")
    except Exception as e:
        bot.reply_to(message, f"❗ Erro ao obter saldo: {str(e)}")

bot.infinity_polling()
