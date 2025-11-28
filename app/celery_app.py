from celery import Celery
from app.config import settings

celery_app = Celery(
    "price_tracker",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=['app.tasks.price_checker']
)

# Configurações
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='America/Sao_Paulo',
    enable_utc=True,
    beat_schedule={
        'check-prices-every-hour': {
            'task': 'app.tasks.price_checker.check_all_products',
            'schedule': settings.scraping_interval_minutes * 60.0,  # Em segundos
        },
    },
)