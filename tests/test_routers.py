# tests/test_routers.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Restaurant Menu API"}

def test_create_food():
    response = client.post("/api/foods/", json={
        "name": "Burger",
        "description": "Tasty burger",
        "price": 5,
        "is_vegan": False,
        "is_special": False,
        "is_publish": True,
        "category_id": 1,
        "toppings": []
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Burger"

def test_read_foods():
    response = client.get("/api/foods/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_read_food():
    response = client.get("/api/foods/1")
    assert response.status_code == 200
    assert response.json()["name"] == "Burger"

def test_update_food():
    response = client.put("/api/foods/1", json={
        "name": "Updated Burger"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Burger"

def test_delete_food():
    response = client.delete("/api/foods/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Food deleted successfully"
