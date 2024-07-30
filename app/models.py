# app/models.py

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from .database import Database

class FoodCategoryModel(Database.Base):
    """
    Модель для категории блюд.
    """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    is_publish = Column(Boolean, default=True)

    foods = relationship("FoodModel", back_populates="category")

class FoodModel(Database.Base):
    """
    Модель для блюда.
    """
    __tablename__ = "foods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer)
    is_vegan = Column(Boolean)
    is_special = Column(Boolean)
    is_publish = Column(Boolean)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("FoodCategoryModel", back_populates="foods")
    toppings = relationship("ToppingModel", back_populates="food")

class ToppingModel(Database.Base):
    """
    Модель для топпинга.
    """
    __tablename__ = "toppings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    food_id = Column(Integer, ForeignKey("foods.id"))

    food = relationship("FoodModel", back_populates="toppings")
