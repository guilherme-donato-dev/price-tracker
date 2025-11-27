from pydantic_settings import BaseSettings
from functools import lru_cache
import secrets


class Settings(BaseSettings):
    database_url: str = "sqlite:///./price_tracker.db"
    
    redis_url: str = "redis://localhost:6379/0"
    
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = "" 
    smtp_password: str = "" 
    
    # App
    secret_key: str = secrets.token_urlsafe(32)
    debug: bool = True
    app_name: str = "Price Tracker API"
    
    # Scraping
    scraping_interval_minutes: int = 60  # Verificar preços a cada 1 hora
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()