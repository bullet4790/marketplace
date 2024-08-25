import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app import models
from app.database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def clear_db():
    # Очищаем базу данных перед каждым тестом
    with TestingSessionLocal() as db:
        for table in reversed(Base.metadata.sorted_tables):
            db.execute(table.delete())
        db.commit()


def test_create_product():
    response = client.post(
        "/products/",
        json={"name": "Test Product", "price": 100, "description": "A test product", "category": "Test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 100

def test_read_product():
    # Сначала создаем продукт
    client.post(
        "/products/",
        json={"name": "Test Product", "price": 100, "description": "A test product", "category": "Test"}
    )
    # Затем проверяем его получение
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"

def test_update_product():
    # Сначала создаем продукт
    client.post(
        "/products/",
        json={"name": "Test Product", "price": 100, "description": "A test product", "category": "Test"}
    )
    # Затем обновляем его
    response = client.put(
        "/products/1",
        json={"name": "Updated Product", "price": 150, "description": "An updated product", "category": "Test"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"
    assert data["price"] == 150

def test_delete_product():
    # Сначала создаем продукт
    client.post(
        "/products/",
        json={"name": "Test Product", "price": 100, "description": "A test product", "category": "Test"}
    )
    # Затем удаляем его
    response = client.delete("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"

def test_filter_products():
    # Сначала создаем продукты
    client.post(
        "/products/",
        json={"name": "Test Product 1", "price": 100, "description": "First test product", "category": "Test"}
    )
    client.post(
        "/products/",
        json={"name": "Test Product 2", "price": 200, "description": "Second test product", "category": "Test"}
    )
    # Затем фильтруем их по имени
    response = client.get("/products/filter/?name=Test Product 1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Product 1"
