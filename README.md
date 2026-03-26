### **Не забудьте про виртуальное окружение!!!**  
Скачивание зависимостей:
````bash
uv sync
````
Запуск:
````bash
uv run uvicorn app.main:app --reload
````
Инициализация:
```Bash
uv run alembic init alembic
```
Применить миграции:
```bash
uv run alembic upgrade head
```

Создать новую миграцию после изменений моделей:
```bash
uv run alembic revision --autogenerate -m "your message"
```

Swagger - http://127.0.0.1:8000/docs