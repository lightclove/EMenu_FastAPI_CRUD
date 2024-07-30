from typing import List, Optional
from pydantic import BaseModel

class ToppingBase(BaseModel):
    """
    Базовая схема для Topping (Топпинг).
    """
    name: str

class ToppingCreate(ToppingBase):
    """
    Схема для создания нового топпинга.
    """
    pass

class ToppingSchema(ToppingBase):
    """
    Схема для чтения топпинга.
    """
    id: int
    food_id: int

    class Config:
        orm_mode = True

class FoodBase(BaseModel):
    """
    Базовая схема для Food (Блюдо).
    """
    name: str
    description: str
    price: int
    is_vegan: bool
    is_special: bool
    is_publish: bool

class FoodCreate(FoodBase):
    """
    Схема для создания нового блюда.
    """
    category_id: int
    toppings: List[ToppingCreate] = []

class FoodUpdate(BaseModel):
    """
    Схема для обновления существующего блюда.
    """
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]
    is_vegan: Optional[bool]
    is_special: Optional[bool]
    is_publish: Optional[bool]
    category_id: Optional[int]
    toppings: Optional[List[ToppingCreate]]

class FoodSchema(FoodBase):
    """
    Схема для чтения блюда.
    """
    id: int
    category_id: int
    toppings: List[ToppingSchema] = []

    class Config:
        orm_mode = True

class FoodCategorySchema(BaseModel):
    """
    Схема для чтения категории блюд.
    """
    id: int
    name: str
    foods: List[FoodSchema] = []

    class Config:
        orm_mode = True
