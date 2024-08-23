# Marketplace API

## Описание

Данный проект представляет собой API для управления записями БД, разработан с использованием FastAPI и SQLAlchemy. Включает эндпоинты для создания, чтения, обновления и удаления продуктов и категорий, а также фильтрацию продуктов по различным параметрам.

## Запуск проекта

1. Клонирование репозитория

                      git clone https://github.com/bullet4790/marketplace.git
   
                      cd marketplace
   
3. Создание и активация виртуального окружения

   Linux:
   
                       python -m venv venv
   
                       source venv/bin/activate
   
   Windows:
   
                       venv\Scripts\activate

5. Установка зависимостей
   
                       pip install -r requirements.txt

6. Запуск сервера FastAPI
   
                       uvicorn app.main:app --reload
   
   При недоступности порта 8000 необходимо использовать другой, например 
 
                       uvicorn app.main:app --reload --port 8094   

8. Открытие в браузере
    
    Swagger UI: http://127.0.0.1:8000/docs 
  
    Главная страница приложения: http://127.0.0.1:8000/

    При использовании другого порта необходимо изменить его номер в адресе

## API Endpoints 

1. Создание записи
   
   - POST /products/
     
2. Получение списка записей БД
   
   - GET /products/
     
     Параметры: skip (количество пропускаемых записей перед началом возврата данных), limit (количество записей в запросе)
     
3. Получение записи по номеру
   
   - GET /products/{product_id}
     
4. Обновление записи
   
   - PUT /products/{product_id}
     
5. Удаление записи
    
   - DELETE /products/{product_id}
     
6. Сортировка получаемых записей
    
   - GET /products/filter/
     
     Параметры: name, category, min_price, max_price, description, skip, limit (позволяют выбирать записи по имени, категории, диапазонам цен, описанию в любых комбинациях)
     
7. Главная страница
    
   - GET /
     
     Загружает файл index.html из папки app/static. Отображает записи БД в виде таблицы.

    
