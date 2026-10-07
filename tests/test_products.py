from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_products():

    response = client.get("/products/")

    assert response.status_code == 200

    products = response.json()

    assert len(products) > 0


def test_get_product():

    response = client.get("/products/1")

    assert response.status_code == 200

    product = response.json()

    assert product["name"] == "Laptop"


def test_product_not_found():

    response = client.get("/products/999")

    assert response.status_code == 200

    assert response.json()["error"] == "Product not found"

def test_create_order():
    response = client.post(
        "/orders/",
        json={
            "product_id": 1,
            "quantity": 2
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 1
    assert data["quantity"] == 2
    assert data["status"] == "created"


def test_create_product():

    response = client.post(
        "/products/",
        json={
            "name": "Monitor",
            "price": 300,
            "stock": 15
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Monitor"
    assert data["price"] == 300
    assert data["stock"] == 15
