from fastapi import FastAPI
from app.database import engine, Base
from app.config import settings

# Importar models para criar tabelas
from app.models import Product, PriceHistory, Alert

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Criar app
app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "message": "Price Tracker API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Importar routers aqui depois que criar
# from app.routers import products, alerts
# app.include_router(products.router)
# app.include_router(alerts.router)