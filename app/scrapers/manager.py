from typing import Optional, Dict
from app.scrapers.generic import GenericScraper
from urllib.parse import urlparse


class ScraperManager:
    """Gerencia qual scraper usar para cada URL"""
    
    def __init__(self):
        self.generic_scraper = GenericScraper()
        # Aqui você pode adicionar scrapers específicos depois
        # self.amazon_scraper = AmazonScraper()
        # self.mercadolivre_scraper = MercadoLivreScraper()
    
    def get_scraper(self, url: str):
        """Retorna o scraper apropriado para a URL"""
        domain = urlparse(url).netloc.lower()
        
        # Adicionar lógica para scrapers específicos
        # if 'amazon' in domain:
        #     return self.amazon_scraper
        # elif 'mercadolivre' in domain or 'mercadolibre' in domain:
        #     return self.mercadolivre_scraper
        
        # Por enquanto, usa o genérico para todos
        return self.generic_scraper
    
    def scrape_product(self, url: str) -> Optional[Dict]:
        """Executa scraping de um produto"""
        scraper = self.get_scraper(url)
        return scraper.scrape(url)


# Instância global
scraper_manager = ScraperManager()