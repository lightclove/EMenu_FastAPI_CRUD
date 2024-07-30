# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


class Database:
    """
    Класс для управления подключением к базе данных и сессиями.
    """

    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()

    def __init__(self):
        """
        Инициализация базы данных и создание всех таблиц.
        """
        self.Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        """
        Создание новой сессии базы данных для использования в каждом запросе.
        """
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
