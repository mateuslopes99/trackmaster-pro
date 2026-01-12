"""
TrackMaster Pro - Sistema de Rastreamento de Encomendas
Backend Flask + Bot Telegram Integrado
Desenvolvido para E-commerce/Dropshipping
"""

from flask import Flask, render_template, jsonify, request
import requests
import threading
from datetime import datetime
import json
import os

# ============================================================================
# CONFIGURAÇÕES
# ============================================================================
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
LINKETRACK_USER = 'teste'
LINKETRACK_TOKEN = '1abcd02b11568202244439c33602d338b15d6560'

app = Flask(__name__)
tracking_history = []
bot_offset = 0

# ============================================================================
# CLASSES E FUNÇÕES (Lógica do Sistema)
# ============================================================================

class LinketrackAPI:
    @staticmethod
    def track_package(tracking_code):
        try:
            url = f"https://api.linketrack.com/track/json"
            params = {'user': LINKETRACK_USER, 'token': LINKETRACK_TOKEN, 'codigo': tracking_code}
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                tracking_history.append({
                    'code': tracking_code,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': data.get('eventos', [{}])[0].get('status', 'Desconhecido') if data.get('eventos') else 'Sem eventos'
                })
                return {'success': True, 'data': data}
            return {'success': False, 'error': f'Erro API: {response.status_code}'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

class TelegramBot:
    @staticmethod
    def send_message(chat_id, text):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, json={'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}, timeout=5)

    @staticmethod
    def get_updates(offset):
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        response = requests.get(url, params={'offset': offset, 'timeout': 30}, timeout=35)
        return response.json() if response.status_code == 200 else None

# ESTA FUNÇÃO PRECISA ESTAR AQUI (SEM ESPAÇOS NO INÍCIO DA LINHA)
def telegram_bot_polling():
    global bot_offset
    print("🤖 Bot do Telegram iniciado!")
    while True:
        try:
            updates = TelegramBot.get_updates(bot_offset)
            if updates and updates.get('ok'):
                for update in updates.get('result', []):
                    bot_offset = update['update_id'] + 1
                    if 'message' in update:
                        chat_id = update['message']['chat']['id']
                        text = update['message'].get('text', '')
                        if text == '/start':
                            TelegramBot.send_message(chat_id, "🚀 <b>TrackMaster Pro Ativo!</b>\nEnvie seu código de rastreio.")
                        elif len(text) > 5:
                            result = LinketrackAPI.track_package(text)
                            if result['success']:
                                status = result['data']['eventos'][0]['status']
                                TelegramBot.send_message(chat_id, f"📦 <b>Status:</b> {status}")
                            else:
                                TelegramBot.send_message(chat_id, "❌ Código não encontrado.")
        except Exception as e:
            print(f"Erro no bot: {e}")

# ============================================================================
# ROTAS E INICIALIZAÇÃO
# ============================================================================

@app.route('/')
def index():
    return render_template('index.html')

def start_bot():
    if TELEGRAM_TOKEN != 'COLE_SEU_TOKEN_AQUI':
        thread = threading.Thread(target=telegram_bot_polling, daemon=True)
        thread.start()
        print("✅ Thread do Bot iniciada!")

# CHAMADA PARA O RENDER
start_bot()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)