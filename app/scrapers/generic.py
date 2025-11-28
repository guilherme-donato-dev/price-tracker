from typing import Optional
from bs4 import BeautifulSoup
import re
from app.scrapers.base import BaseScraper


class GenericScraper(BaseScraper):
    """Scraper genérico que tenta encontrar preços em qualquer site"""
    
    def extract_price(self, soup: BeautifulSoup) -> Optional[float]:
        """Tenta extrair preço de forma genérica"""
        
        # Padrões comuns de preço
        price_patterns = [
            r'R\$\s*(\d+(?:\.\d{3})*,\d{2})',  # R$ 1.234,56
            r'(\d+(?:\.\d{3})*,\d{2})',         # 1.234,56
            r'(\d+,\d{2})',                      # 123,45
        ]
        
        # Seletores comuns para preço
        price_selectors = [
            {'class': re.compile(r'price', re.I)},
            {'class': re.compile(r'preco', re.I)},
            {'itemprop': 'price'},
            {'data-testid': re.compile(r'price', re.I)},
        ]
        
        # Tentar encontrar preço pelos seletores
        for selector in price_selectors:
            elements = soup.find_all(attrs=selector)
            for element in elements:
                text = element.get_text()
                for pattern in price_patterns:
                    match = re.search(pattern, text)
                    if match:
                        price_str = match.group(1)
                        # Converter formato BR para float
                        price_str = price_str.replace('.', '').replace(',', '.')
                        try:
                            return float(price_str)
                        except ValueError:
                            continue
        
        # Tentar encontrar no texto geral
        text = soup.get_text()
        for pattern in price_patterns:
            matches = re.findall(pattern, text)
            if matches:
                try:
                    price_str = matches[0].replace('.', '').replace(',', '.')
                    return float(price_str)
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrai o nome do produto"""
        
        # Tentar title da página
        title = soup.find('title')
        if title:
            return title.get_text().strip()
        
        # Tentar h1
        h1 = soup.find('h1')
        if h1:
            return h1.get_text().strip()
        
        return None
    
    def extract_image(self, soup: BeautifulSoup) -> Optional[str]:
        """Extrai URL da imagem principal"""
        
        # Tentar Open Graph
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            return og_image['content']
        
        # Tentar primeira imagem grande
        images = soup.find_all('img')
        for img in images:
            src = img.get('src') or img.get('data-src')
            if src and ('product' in src.lower() or 'item' in src.lower()):
                return src
        
        return None