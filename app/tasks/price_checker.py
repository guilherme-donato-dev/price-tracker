from app.celery_app import celery_app
from app.database import SessionLocal
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.scrapers.manager import scraper_manager
from app.notifications.telegram import telegram_notifier
from datetime import datetime


@celery_app.task
def check_product_price(product_id: int):
    """Verifica o preço de um produto específico"""
    db = SessionLocal()
    
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        
        if not product or not product.is_active:
            return
        
        # Fazer scraping
        result = scraper_manager.scrape_product(product.url)
        
        if not result or not result.get('price'):
            return
        
        new_price = result['price']
        old_price = product.current_price
        
        # Salvar histórico
        price_entry = PriceHistory(
            product_id=product.id,
            price=new_price,
            is_available=result.get('is_available', True)
        )
        db.add(price_entry)
        
        # Atualizar produto
        product.current_price = new_price
        product.last_checked = datetime.utcnow()
        
        if not product.image_url and result.get('image_url'):
            product.image_url = result['image_url']
        
        # Verificar alertas
        should_notify = False
        
        # Alerta de queda de preço (qualquer queda)
        if old_price and new_price < old_price:
            should_notify = True
            telegram_notifier.send_price_drop_alert(
                product_name=product.name,
                old_price=old_price,
                new_price=new_price,
                url=product.url
            )
        
        # Alerta de preço alvo
        if product.target_price and new_price <= product.target_price:
            if not old_price or old_price > product.target_price:
                telegram_notifier.send_target_price_alert(
                    product_name=product.name,
                    target_price=product.target_price,
                    current_price=new_price,
                    url=product.url
                )
        
        db.commit()
        
    except Exception as e:
        print(f"Erro ao verificar produto {product_id}: {e}")
        db.rollback()
    finally:
        db.close()


@celery_app.task
def check_all_products():
    """Verifica o preço de todos os produtos ativos"""
    db = SessionLocal()
    
    try:
        products = db.query(Product).filter(Product.is_active == True).all()
        
        for product in products:
            check_product_price.delay(product.id)
        
        print(f"Iniciada verificação de {len(products)} produtos")
        
    finally:
        db.close()