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

# ============================================================================
# CONFIGURAÇÕES - COLE SUAS CREDENCIAIS AQUI
# ============================================================================

# Token do Bot do Telegram (obtenha com @BotFather)
TELEGRAM_TOKEN = '8324151299:AAGz29_MZRbv6R-kZJQAschx3AObKrN_2uU'

# Credenciais da API Linketrack
LINKETRACK_USER = 'teste'
LINKETRACK_TOKEN = '1abcd02b11568202244439c33602d338b15d6560'

# ============================================================================

app = Flask(__name__)

# Armazenamento em memória (simples para PythonAnywhere)
tracking_history = []
bot_offset = 0


class LinketrackAPI:
    """Classe para interagir com a API da Linketrack"""
    
    BASE_URL = "https://api.linketrack.com"
    
    @staticmethod
    def track_package(tracking_code):
        """
        Rastreia um pacote usando a API da Linketrack
        
        Args:
            tracking_code (str): Código de rastreamento
            
        Returns:
            dict: Dados do rastreamento ou erro
        """
        try:
            url = f"{LinketrackAPI.BASE_URL}/track/json"
            params = {
                'user': LINKETRACK_USER,
                'token': LINKETRACK_TOKEN,
                'codigo': tracking_code
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Adiciona ao histórico
                tracking_history.append({
                    'code': tracking_code,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'status': data.get('eventos', [{}])[0].get('status', 'Desconhecido') if data.get('eventos') else 'Sem eventos',
                    'data': data
                })
                
                return {
                    'success': True,
                    'data': data
                }
            else:
                return {
                    'success': False,
                    'error': f'Erro na API: {response.status_code}'
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


class TelegramBot:
    """Classe para gerenciar o Bot do Telegram"""
    
    @staticmethod
    def send_message(chat_id, text, parse_mode='HTML'):
        """Envia mensagem via Telegram"""
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {
                'chat_id': chat_id,
                'text': text,
                'parse_mode': parse_mode
            }
            requests.post(url, json=payload, timeout=5)
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
    
    @staticmethod
    def get_updates(offset):
        """Obtém atualizações do Telegram"""
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
            params = {'offset': offset, 'timeout': 30}
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Erro ao obter updates: {e}")
            return None
    
    @staticmethod
    def format_tracking_card(tracking_data):
        """Formata os dados de rastreamento em um card bonito"""
        if not tracking_data.get('success'):
            return f"❌ <b>Erro ao rastrear</b>\n\n{tracking_data.get('error', 'Erro desconhecido')}"
        
        data = tracking_data['data']
        codigo = data.get('codigo', 'N/A')
        
        message = f"📦 <b>TrackMaster Pro</b>\n"
        message += f"━━━━━━━━━━━━━━━━━━━━\n\n"
        message += f"🔖 <b>Código:</b> <code>{codigo}</code>\n\n"
        
        eventos = data.get('eventos', [])
        
        if eventos:
            message += f"📍 <b>Status Atual:</b>\n"
            ultimo = eventos[0]
            message += f"   {ultimo.get('status', 'N/A')}\n"
            message += f"   📅 {ultimo.get('data', 'N/A')}\n"
            message += f"   🏢 {ultimo.get('local', 'N/A')}\n\n"
            
            if len(eventos) > 1:
                message += f"📋 <b>Histórico:</b>\n"
                for i, evento in enumerate(eventos[1:4], 1):  # Mostra até 3 eventos anteriores
                    message += f"\n{i}. {evento.get('status', 'N/A')}\n"
                    message += f"   📅 {evento.get('data', 'N/A')}\n"
                
                if len(eventos) > 4:
                    message += f"\n... e mais {len(eventos) - 4} eventos\n"
        else:
            message += "ℹ️ <b>Nenhum evento encontrado</b>\n"
        
        message += f"\n━━━━━━━━━━━━━━━━━━━━\n"
        message += f"✅ Rastreado via TrackMaster Pro"
        
        return message
    
    @staticmethod
    def process_message(message):
        """Processa mensagens recebidas"""
        chat_id = message['chat']['id']
        text = message.get('text', '')
        
        if text == '/start':
            welcome_msg = """
🚀 <b>Bem-vindo ao TrackMaster Pro!</b>

Seu assistente profissional de rastreamento de encomendas.

━━━━━━━━━━━━━━━━━━━━

📦 <b>Como usar:</b>
   Envie um código de rastreamento e receba informações detalhadas instantaneamente.

💼 <b>Recursos:</b>
   ✓ Rastreamento em tempo real
   ✓ Histórico completo
   ✓ Notificações automáticas
   ✓ Suporte 24/7

━━━━━━━━━━━━━━━━━━━━

Desenvolvido para E-commerce & Dropshipping
            """
            TelegramBot.send_message(chat_id, welcome_msg)
        
        elif text and len(text) > 5:  # Assume que é um código de rastreamento
            # Envia mensagem de processamento
            TelegramBot.send_message(chat_id, "🔍 <b>Rastreando encomenda...</b>")
            
            # ============================================================================
# INICIALIZAÇÃO - AJUSTADA PARA RENDER/GUNICORN
# ============================================================================

# Função para iniciar o bot de forma segura
def telegram_bot_polling():
    """Loop de polling do bot do Telegram"""
    global bot_offset
    print("🤖 Bot do Telegram iniciado!")
    
    while True:
        try:
            # Esta parte usa a lógica que você já tinha criado
            updates = TelegramBot.get_updates(bot_offset)
            
            if updates and updates.get('ok'):
                for update in updates.get('result', []):
                    bot_offset = update['update_id'] + 1
                    if 'message' in update:
                        TelegramBot.process_message(update['message'])
        
        except Exception as e:
            print(f"Erro no bot: {e}")
def start_bot():
    if TELEGRAM_TOKEN != 'COLE_SEU_TOKEN_AQUI':
        # daemon=True garante que o bot morra se o app principal parar
        bot_thread = threading.Thread(target=telegram_bot_polling, daemon=True)
        bot_thread.start()
        print("✅ Thread do Bot iniciada com sucesso!")
    else:
        print("⚠️ AVISO: Configure o TELEGRAM_TOKEN para ativar o bot!")

# CHAMADA DIRETA (Fora do if __name__ == '__main__')
# Isso garante que o Gunicorn execute o bot ao subir o site
start_bot()

if __name__ == '__main__':
    # Isso só roda no seu computador (localhost)
    print("🚀 Iniciando em modo de desenvolvimento...")
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
