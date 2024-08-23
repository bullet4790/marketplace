from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from . import models, schemas, crud
from .database import SessionLocal, engine

# Создаем таблицы в базе данных
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Product API")
app.mount("/static", StaticFiles(directory="app/static"), name="static")


# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Создание продукта
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)


# Получение продукта по ID
@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# Получение списка продуктов
@app.get("/products/", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products


# Обновление продукта
@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: int, product: schemas.ProductUpdate, db: Session = Depends(get_db)):
    db_product = crud.update_product(db, product_id=product_id, product=product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# Удаление продукта
@app.delete("/products/{product_id}", response_model=schemas.Product)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.delete_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# Фильтрация продуктов по параметрам
@app.get("/products/filter/", response_model=List[schemas.Product])
def filter_products(
        name: Optional[str] = Query(None),
        category: Optional[str] = Query(None),
        min_price: Optional[int] = Query(None),
        max_price: Optional[int] = Query(None),
        description: Optional[str] = Query(None),
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
):
    query = db.query(models.Product)

    if name:
        query = query.filter(models.Product.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(models.Product.category.ilike(f"%{category}%"))
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    if description:
        query = query.filter(models.Product.description.ilike(f"%{description}%"))

    products = query.offset(skip).limit(limit).all()
    return products

# Главная страница - index.html
@app.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse("app/static/index.html")