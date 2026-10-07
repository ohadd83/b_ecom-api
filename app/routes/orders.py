from fastapi import APIRouter, HTTPException

from app.database import products_db, orders_db
from app.models import Order


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.get("/")
def get_orders():
    return orders_db


@router.post("/")
def create_order(order: Order):

    # Find product
    product = None

    for item in products_db:

        if item["id"] == order.product_id:
            product = item
            break

    # Product doesn't exist
    if product is None:

        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    # Check stock
    if product["stock"] < order.quantity:

        raise HTTPException(
            status_code=400,
            detail="Not enough stock"
        )

    # Reduce stock
    product["stock"] -= order.quantity

    # Create order
    new_order = {
        "id": len(orders_db) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "created"
    }

    orders_db.append(new_order)

    return new_order
