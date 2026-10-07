from fastapi import APIRouter

from app.database import products_db
from app.models import Product


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def get_products():
    return products_db


@router.get("/{product_id}")
def get_product(product_id: int):

    for product in products_db:

        if product["id"] == product_id:
            return product

    return {
        "error": "Product not found"
    }


@router.post("/")
def create_product(product: Product):

    new_product = {
        "id": len(products_db) + 1,
        "name": product.name,
        "price": product.price,
        "stock": product.stock
    }

    products_db.append(new_product)

    return new_product
