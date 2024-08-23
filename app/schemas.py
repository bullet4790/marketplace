from typing import Optional
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
