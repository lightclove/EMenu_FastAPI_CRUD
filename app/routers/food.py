from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import Database
from app.models import FoodModel
from app.schemas import FoodCreate, FoodUpdate, FoodSchema, FoodCategorySchema
from app.crud import FoodCRUD


class FoodRouter:
    """
    Класс для управления маршрутами для сущности Food.
    """

    def __init__(self):
        """
        Инициализация роутера и базы данных.
        """
        self.router = APIRouter()
        self.database = Database()

        @self.router.get("/foods/", response_model=List[FoodCategorySchema])
        def read_foods(is_vegan: Optional[bool] = None, is_special: Optional[bool] = None,
                       toppings: Optional[List[str]] = None, db: Session = Depends(self.database.get_db)):
            """
            Получить все опубликованные блюда с возможностью фильтрации по is_vegan, is_special и toppings.
            """
            food_crud = FoodCRUD(db)
            foods = food_crud.get_foods(is_vegan=is_vegan, is_special=is_special, toppings=toppings)
            categories = {}
            for food in foods:
                if food.category_id not in categories:
                    categories[food.category_id] = {
                        "id": food.category_id,
                        "name": food.category.name,
                        "foods": []
                    }
                categories[food.category_id]["foods"].append(food)
            return list(categories.values())

        @self.router.post("/foods/", response_model=FoodSchema)
        def create_food(food: FoodCreate, db: Session = Depends(self.database.get_db)):
            """
            Создать новое блюдо.
            """
            food_crud = FoodCRUD(db)
            return food_crud.create_food(food)

        @self.router.get("/foods/{food_id}", response_model=FoodSchema)
        def read_food(food_id: int, db: Session = Depends(self.database.get_db)):
            """
            Получить информацию о блюде по его ID.
            """
            food_crud = FoodCRUD(db)
            return food_crud.get_food(food_id)

        @self.router.put("/foods/{food_id}", response_model=FoodSchema)
        def update_food(food_id: int, food: FoodUpdate, db: Session = Depends(self.database.get_db)):
            """
            Обновить информацию о блюде.
            """
            food_crud = FoodCRUD(db)
            return food_crud.update_food(food_id, food)

        def delete_food(food_id: int, db: Session = Depends(self.database.get_db)):
            """
            Удалить блюдо.
            """
            food_crud = FoodCRUD(db)
            success = food_crud.delete_food(food_id)
            if not success:
                raise HTTPException(status_code=404, detail="Food not found")
            return {"message": "Food deleted successfully"}


# Инициализация и создание объекта роутера
food_router = FoodRouter().router
