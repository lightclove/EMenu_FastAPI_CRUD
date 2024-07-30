# tests/test_crud.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Database
from app.models import FoodModel, FoodCategoryModel, ToppingModel
from app.schemas import FoodCreate, FoodUpdate
from app.crud import FoodCRUD

# Настройка базы данных для тестов
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    Database.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Database.Base.metadata.drop_all(bind=engine)

def test_create_food(db):
    food_crud = FoodCRUD(db)
    food = FoodCreate(name="Pizza", description="Delicious pizza", price=10, is_vegan=False, is_special=True, is_publish=True, category_id=1, toppings=[])
    db_food = food_crud.create_food(food)
    assert db_food.name == "Pizza"

def test_get_food(db):
    food_crud = FoodCRUD(db)
    food = food_crud.get_food(1)
    assert food is not None
    assert food.name == "Pizza"

def test_update_food(db):
    food_crud = FoodCRUD(db)
    update_data = FoodUpdate(name="Updated Pizza")
    food = food_crud.update_food(1, update_data)
    assert food.name == "Updated Pizza"

def test_delete_food(db):
    food_crud = FoodCRUD(db)
    success = food_crud.delete_food(1)
    assert success
