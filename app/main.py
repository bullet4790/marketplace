# app/main.py
from typing import List
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from . import crud, models, plan, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=plan.Product)
def create_product(product: plan.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products/{product_id}", response_model=plan.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

# Новый маршрут для получения всех продуктов
@app.get("/products", response_model=List[plan.Product])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)

@app.put("/products/{product_id}", response_model=plan.Product)
def update_product(product_id: int, product: plan.ProductCreate, db: Session = Depends(get_db)):
    return crud.update_product(db=db, product_id=product_id, product=product)

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    return crud.delete_product(db=db, product_id=product_id)

@app.get("/", response_class=HTMLResponse)
async def read_index():
    try:
        with open("app/static/index.html") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Index file not found")
