# app/crud.py

from sqlalchemy.orm import Session
from typing import List, Optional
from .models import FoodModel, ToppingModel
from .schemas import FoodCreate, FoodUpdate


class FoodCRUD:
    """
    Класс для реализации операций CRUD (Create, Read, Update, Delete) для сущности Food (Блюдо).
    """

    def __init__(self, db: Session):
        """
        Инициализация сессии базы данных.
        """
        self.db = db

    def create_food(self, food: FoodCreate) -> FoodModel:
        """
        Создать новое блюдо.
        """
        db_food = FoodModel(
            name=food.name,
            description=food.description,
            price=food.price,
            is_vegan=food.is_vegan,
            is_special=food.is_special,
            is_publish=food.is_publish,
            category_id=food.category_id
        )
        self.db.add(db_food)
        self.db.commit()
        self.db.refresh(db_food)

        for topping in food.toppings:
            db_topping = ToppingModel(name=topping.name, food_id=db_food.id)
            self.db.add(db_topping)

        self.db.commit()
        return db_food

    def get_food(self, food_id: int) -> Optional[FoodModel]:
        """
        Получить блюдо по его ID.
        """
        return self.db.query(FoodModel).filter(FoodModel.id == food_id).first()

    def get_foods(self, is_vegan: Optional[bool] = None, is_special: Optional[bool] = None,
                  toppings: Optional[List[str]] = None) -> List[FoodModel]:
        """
        Получить все опубликованные блюда с возможностью фильтрации по is_vegan, is_special и toppings.
        """
        query = self.db.query(FoodModel).filter(FoodModel.is_publish == True)

        if is_vegan is not None:
            query = query.filter(FoodModel.is_vegan == is_vegan)

        if is_special is not None:
            query = query.filter(FoodModel.is_special == is_special)

        if toppings:
            query = query.join(FoodModel.toppings).filter(ToppingModel.name.in_(toppings))

        return query.all()

    def update_food(self, food_id: int, food: FoodUpdate) -> Optional[FoodModel]:
        """
        Обновить информацию о блюде.
        """
        db_food = self.get_food(food_id)
        if not db_food:
            return None

        for var, value in vars(food).items():
            if value is not None:
                setattr(db_food, var, value)

        self.db.commit()
        self.db.refresh(db_food)
        return db_food

    def delete_food(self, food_id: int) -> bool:
        """
        Удалить блюдо.
        """
        db_food = self.get_food(food_id)
        if not db_food:
            return False

        self.db.delete(db_food)
        self.db.commit()
        return True
