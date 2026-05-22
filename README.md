# K-Metric | Observability Dashboard

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/Frontend-React_19-61DAFB?logo=react)
![Flask](https://img.shields.io/badge/Backend-Flask_3.0-000000?logo=flask)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?logo=postgresql)

**K-Metric** — это современная система мониторинга фоновых задач и производительности API. Проект разработан как демонстрация навыков Fullstack-разработки (Flask/React/TS) с фокусом на оптимизацию работы с данными и высокую производительность интерфейса.

---

## 🚀 Основные возможности

- **Dashboard:** Визуализация среднего времени ответа API (Latency) и статусов фоновых задач.
- **SQL Optimization:** Использование **SQL Views** для мгновенной агрегации метрик без нагрузки на серверную логику.
- **State Management:** Легкое и быстрое управление состоянием через **Zustand**.
- **Security:** Авторизация на базе **JWT** с защищенными роутами.
- **Automation:** Встроенный фоновый воркер для симуляции нагрузки и генерации данных.
- **Testing:** Покрытие тестами на **Pytest** (Backend) и **Vitest** (Frontend).

---

## 🛠 Технологический стек

### Backend

- **Framework:** Flask (Application Factory pattern)
- **ORM:** SQLAlchemy + Flask-Migrate (Alembic)
- **Auth:** PyJWT + Bcrypt
- **Testing:** Pytest + Pytest-Flask

### Frontend

- **Framework:** React 19 + TypeScript + Vite
- **Styling:** Tailwind CSS v4
- **State:** Zustand (Store-based architecture)
- **Charts:** Recharts
- **Testing:** Vitest + JSDOM

---

## 🚦 Быстрый старт

### 1. Подготовка окружения

Склонируйте репозиторий и запустите базу данных через Docker:

```bash
docker-compose up -d
```

### 2. Настройка Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade          # Применение миграций и создание SQL View
python seed.py            # Создание админа (admin/admin123) и демо-данных
python run.py             # Запуск сервера на порту 5001
```

### 3. Настройка Frontend

```bash
cd frontend
npm install
npm run dev               # Запуск UI на порту 5173
```

### 4. Симуляция данных (опционально)

Чтобы увидеть живую динамику на графиках, запустите воркер:

```bash
python backend/worker.py
```

---

## 🧪 Тестирование

### Backend (Pytest)

```bash
cd backend
pytest
```

### Frontend (Vitest)

```bash
cd frontend
npm test
```

---

## 📐 Архитектурные решения (Education Purpose)

1.  **SQL Views:** Для расчета среднего времени ответа API используется представление в PostgreSQL. Это позволяет выполнять тяжелые расчеты на стороне БД, отдавая фронтенду уже готовый результат.
2.  **Zustand Store:** Выбран вместо Context API для исключения лишних ре-рендеров и более чистой архитектуры без "Prop Drilling".
3.  **Tailwind v4:** Используется самая свежая версия CSS-фреймворка с поддержкой JIT и упрощенной конфигурацией через `@import`.
4.  **Application Factory:** Структура Flask-приложения позволяет легко масштабировать проект и упрощает тестирование.

--
