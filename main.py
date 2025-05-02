import os
from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
    return '✅ Bot rodando (teste).'


@app.route('/<token>', methods=['POST'])
def webhook(token):
    data = request.get_json()
    print('📥 Recebido do Telegram:', data)
    return 'ok'


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
