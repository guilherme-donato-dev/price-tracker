from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.product import Product
from app.models.price_history import PriceHistory
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductWithHistory
from datetime import datetime
from app.scrapers.manager import scraper_manager

router = APIRouter(
    prefix="/products",
    tags=["products"]
)


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Cria um novo produto para monitorar"""
    
    # Verificar se URL já existe
    existing = db.query(Product).filter(Product.url == product.url).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Produto com esta URL já existe"
        )
    
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/", response_model=List[ProductResponse])
def list_products(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db)
):
    """Lista todos os produtos"""
    query = db.query(Product)
    
    if active_only:
        query = query.filter(Product.is_active == True)
    
    products = query.offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductWithHistory)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Busca um produto específico com histórico de preços"""
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db)
):
    """Atualiza um produto"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    # Atualizar apenas campos fornecidos
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_product, field, value)
    
    db_product.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    """Deleta um produto"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    db.delete(db_product)
    db.commit()
    return None


@router.post("/{product_id}/check-price", response_model=ProductResponse)
def check_price_now(product_id: int, db: Session = Depends(get_db)):
    """Força verificação de preço imediata"""
    db_product = db.query(Product).filter(Product.id == product_id).first()
    
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    # Executar scraping
    result = scraper_manager.scrape_product(db_product.url)
    
    if result and result.get('price'):
        # Atualizar preço atual
        db_product.current_price = result['price']
        db_product.last_checked = datetime.utcnow()
        
        # Salvar no histórico
        price_entry = PriceHistory(
            product_id=db_product.id,
            price=result['price'],
            is_available=result.get('is_available', True)
        )
        db.add(price_entry)
        
        # Atualizar imagem se não tiver
        if not db_product.image_url and result.get('image_url'):
            db_product.image_url = result['image_url']
        
        db.commit()
        db.refresh(db_product)
    
    return db_product