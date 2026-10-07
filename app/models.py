from pydantic import BaseModel, Field


class Product(BaseModel):
    name: str
    price: float
    stock: int


class Order(BaseModel):
    product_id: int
    quantity: int  = Field(gt=0)
