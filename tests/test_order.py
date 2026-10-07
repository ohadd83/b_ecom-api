from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


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


def test_create_order_product_not_found():

    response = client.post(
        "/orders/",
        json={
            "product_id": 999,
            "quantity": 2
        }
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Product not found"


def test_create_order_insufficient_stock():

    response = client.post(
        "/orders/",
        json={
            "product_id": 1,
            "quantity": 1000
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Not enough stock"


def test_create_order_reduces_stock():

    # Get current stock
    response = client.get("/products/1")

    initial_stock = response.json()["stock"]

    # Create order
    order_quantity = 2

    response = client.post(
        "/orders/",
        json={
            "product_id": 1,
            "quantity": order_quantity
        }
    )

    assert response.status_code == 200

    # Check stock again
    response = client.get("/products/1")

    final_stock = response.json()["stock"]

    assert final_stock == initial_stock - order_quantity


def test_create_order_quantity_zero():

    response = client.post(
        "/orders/",
        json={
            "product_id": 1,
            "quantity": 0
        }
    )

    assert response.status_code == 422


def test_create_order_negative_quantity():

    response = client.post(
        "/orders/",
        json={
            "product_id": 1,
            "quantity": -5
        }
    )

    assert response.status_code == 422


def test_create_order_missing_product_id():

    response = client.post(
        "/orders/",
        json={
            "quantity": 2
        }
    )

    assert response.status_code == 422


def test_create_order_missing_quantity():

    response = client.post(
        "/orders/",
        json={
            "product_id": 1
        }
    )

    assert response.status_code == 422


def test_create_order_wrong_quantity_type():

    response = client.post(
        "/orders/",
        json={
            "product_id": 1,
            "quantity": "hello"
        }
    )

    assert response.status_code == 422
