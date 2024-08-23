from sqlalchemy import Column, Integer, String
from .database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    category = Column(String, nullable=True)
    price = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
