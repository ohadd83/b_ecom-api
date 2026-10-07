from fastapi import FastAPI

from app.routes import products
from app.routes import orders


app = FastAPI(
    title="E-Commerce API prd",
    version="1.0.0"
)


app.include_router(products.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {
        "application": "E-Commerce API",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
