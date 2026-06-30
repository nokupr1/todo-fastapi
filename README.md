# ✅ QuickDo

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D)](https://vuejs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![uv](https://img.shields.io/badge/uv-000000?style=for-the-badge&logo=python&logoColor=white)](https://github.com/astral-sh/uv)

**QuickDo** — это лаконичное, быстрое и современное приложение для управления задачами. Создано с акцентом на удобство использования, минималистичный дизайн и высокую скорость работы благодаря асинхронному бэкенду.

![QuickDo Screenshot](<img width="1768" height="1086" alt="image" src="https://github.com/user-attachments/assets/e1fd0640-8577-4c56-bc22-dfa5ee62b269"/>)

---

## ✨ Ключевые особенности

* **Умная сортировка:** Актуальные задачи всегда наверху, выполненные уходят вниз и становятся полупрозрачными.
* **Темы оформления:** Поддержка светлой и приятной темной темы (Soft Dark) с сохранением выбора пользователя.
* **Мгновенный отклик:** Использование Vue 3 Composition API делает интерфейс невероятно отзывчивым.
* **RESTful API:** Надежный и строгий бэкенд с автоматической документацией Swagger.

---

## 🛠 Технологический стек

**Frontend:**
* Vue 3
* Vite
* Tailwind CSS

**Backend:**
* Python 3.13
* FastAPI
* SQLAlchemy (ORM)
* Uvicorn
* uv (сверхбыстрый пакетный менеджер)

---

## 🚀 Инструкция по локальному развертыванию

Для запуска приложения на вашем ПК убедитесь, что у вас установлены **Python 3.13+**, **Node.js 18+** и менеджер пакетов **[uv](https://docs.astral.sh/uv/)**.

### 1. Запуск Backend (FastAPI)

Откройте терминал в папке бэкенда (или корневой папке проекта, где находится `pyproject.toml`) и выполните следующие команды:

**Синхронизация зависимостей:**
*(uv автоматически создаст виртуальное окружение `.venv` и мгновенно установит все нужные пакеты из `uv.lock`)*
```bash
uv sync
```

Запуск сервера:
```bash
uv run run.py
```

Бэкенд будет доступен по адресу: http://localhost:8000
Интерактивная документация (Swagger): http://localhost:8000/api/docs

### 2. Запуск Frontend (Vue 3)
Откройте новое окно терминала (не закрывая бэкенд) и перейдите в папку фронтенда:
```bash
cd frontend
```

**Установка зависимостей:**
```bash
npm install
```

**Запуск сервера разработки:**
```bash
npm run dev
```
Приложение откроется в вашем браузере по адресу: http://localhost:5173
