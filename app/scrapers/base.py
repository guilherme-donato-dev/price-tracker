from abc import ABC, abstractmethod
from typing import Optional, Dict
import requests
from bs4 import BeautifulSoup
from app.config import settings


class BaseScraper(ABC):
    """Classe base para scrapers"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': settings.user_agent,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
        }
    
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Busca e retorna o HTML da página"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            print(f"Erro ao buscar página {url}: {e}")
            return None
    
    @abstractmethod
    def extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Extrai o preço da página"""
        pass
    
    @abstractmethod
    def extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrai o nome do produto"""
        pass
    
    def extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrai URL da imagem (opcional)"""
        return None
    
    def scrape(self, url: str) -> Optional[Dict]:
        """Executa o scraping completo"""
        soup = self.fetch_page(url)
        if not soup:
            return None
        
        try:
            price = self.extract_price(soup)
            name = self.extract_name(soup)
            image = self.extract_image(soup)
            
            return {
                'price': price,
                'name': name,
                'image_url': image,
                'is_available': price is not None
            }
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
            return None