import ccxt
import telebot

# Credenciais fixas
api_key = 'mx0vgl25FDEAdQxYh5'
api_secret = '54ace640205a4dc2a8188b4e58132ca6'
telegram_token = '7141208046:AAER6JutMbcixWVsoVRj6Sb8zXo8qV8PJj8'

bot = telebot.TeleBot(telegram_token)

exchange = ccxt.mexc({
    'apiKey': api_key,
    'secret': api_secret,
    'options': {
        'defaultType': 'swap'  # FUTUROS (mudei aqui para swap que é o certo na MEXC)
    }
})

# Função para puxar saldo completo (total, livre e em uso)
def get_total_balance():
    try:
        balance = exchange.fetch_balance()
        usdt_info = balance['total'].get('USDT', 0)
        free_usdt = balance['free'].get('USDT', 0)
        used_usdt = balance['used'].get('USDT', 0)
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
