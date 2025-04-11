# 🗒️ Note API — FastAPI Pet-проєкт

Простий REST API для нотаток, побудований на FastAPI, SQLAlchemy та JWT-аутентифікації.

---

## 🚀 Можливості
- Реєстрація та логін користувачів із безпечним збереженням паролів (bcrypt)
- Аутентифікація на основі JWT + OAuth2
- Повноцінні CRUD-операції з нотатками
- SQLite база даних через SQLAlchemy ORM
- Swagger-документація за адресою `/docs`

---

## 📦 Встановлення

```bash
# Клонувати репозиторій
https://github.com/AvgDeftonesEnjoyer/note_api_pet.git
cd note-api

# Створити віртуальне середовище (опційно)
python -m venv venv
venv\Scripts\activate  # Windows

# Встановити залежності
pip install -r requirements.txt

# Запустити сервер
uvicorn main:app --reload
```

---

## 🔐 Інструкція з авторизації (Swagger UI)

### 1. Зареєструвати нового користувача
`POST /auth/register`
```json
{
  "username": ".......",
  "email": "test@example.com",
  "password": "......."
}
```

### 2. Увійти (логін)
`POST /auth/login`
Потрібно ввести логін і пароль у формі:
- `username=.......`
- `password=.......`

Отримаєш відповідь:
```json
{
  "access_token": "токен",
  "token_type": "bearer"
}
```

### 3. Авторизація у Swagger UI
- Натисни кнопку **Authorize** зверху
- Введи логін та пароль
- Swagger автоматично підтягне токен у запити

### 4. Тестування захищених маршрутів
- `GET /profile`
- `GET /notes/`
- `POST /notes/`
- `PUT /notes/{id}`
- `DELETE /notes/{id}`

---

## 📁 Структура проєкту
```
note_api/
├── routers/
│   ├── auth.py
│   └── notes.py
├── models/
│   ├── user.py
│   └── note.py
├── schemas/
│   ├── user.py
│   └── note.py
├── database.py
├── main.py
```

---

## 🛡 Залежності
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- Passlib (bcrypt)
- python-jose (JWT)

---

## 💬 Автор
Олексій Шапка — 2025
