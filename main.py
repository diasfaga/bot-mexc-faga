import ccxt
import os
import telebot

# Configurações a partir de variáveis de ambiente
api_key = os.getenv('MEXC_API_KEY')
api_secret = os.getenv('MEXC_API_SECRET')
telegram_token = os.getenv('TELEGRAM_TOKEN')

bot = telebot.TeleBot(telegram_token)

exchange = ccxt.mexc({
    'apiKey': api_key,
    'secret': api_secret,
    'options': {
        'defaultType': 'future'
    }
})

# Função para puxar saldo completo
def get_total_balance():
    try:
        balance = exchange.fetch_balance()
        usdt_info = balance['total']['USDT']
        free_usdt = balance['free']['USDT']
        used_usdt = balance['used']['USDT']
        return f"💰 Total USDT: {usdt_info}\n✅ Livre: {free_usdt}\n📊 Em uso: {used_usdt}"
    except Exception as e:
        return f"❗ Erro ao obter saldo: {str(e)}"

# Comandos do Telegram
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Bot de futuros MEXC online e pronto!")

@bot.message_handler(commands=['balance'])
def balance(message):
    result = get_total_balance()
    bot.reply_to(message, result)

# Inicia o polling
if __name__ == '__main__':
    bot.polling()
