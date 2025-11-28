import requests
from app.config import settings
from typing import Optional


class TelegramNotifier:
    """Envia notificações via Telegram"""
    
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.chat_id = settings.telegram_chat_id
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def send_message(self, message: str) -> bool:
        """Envia uma mensagem no Telegram"""
        if not self.bot_token or not self.chat_id:
            print("Telegram não configurado")
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            data = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            response = requests.post(url, json=data, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Erro ao enviar mensagem Telegram: {e}")
            return False
    
    def send_price_drop_alert(
        self,
        product_name: str,
        old_price: float,
        new_price: float,
        url: str
    ) -> bool:
        """Envia alerta de queda de preço"""
        percent_drop = ((old_price - new_price) / old_price) * 100
        
        message = f"""
🔔 <b>ALERTA DE PREÇO!</b>

📦 <b>Produto:</b> {product_name}

💰 <b>Preço Anterior:</b> R$ {old_price:.2f}
💸 <b>Novo Preço:</b> R$ {new_price:.2f}
📉 <b>Economia:</b> R$ {old_price - new_price:.2f} ({percent_drop:.1f}%)

🔗 <a href="{url}">Ver produto</a>
        """
        
        return self.send_message(message.strip())
    
    def send_target_price_alert(
        self,
        product_name: str,
        target_price: float,
        current_price: float,
        url: str
    ) -> bool:
        """Envia alerta quando atinge preço alvo"""
        message = f"""
🎯 <b>PREÇO ALVO ATINGIDO!</b>

📦 <b>Produto:</b> {product_name}

🎯 <b>Preço Alvo:</b> R$ {target_price:.2f}
💰 <b>Preço Atual:</b> R$ {current_price:.2f}

🔗 <a href="{url}">Comprar agora!</a>
        """
        
        return self.send_message(message.strip())


# Instância global
telegram_notifier = TelegramNotifier()