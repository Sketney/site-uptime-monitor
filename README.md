# 🌐 Site Uptime Monitor

![CI/CD](https://github.com/Sketney/site-uptime-monitor/actions/workflows/ci-cd.yml/badge.svg)

**Site Uptime Monitor** — сервис для проверки доступности веб-сайтов с сохранением истории в базу данных.  
Реализован на **FastAPI**, использует **PostgreSQL** и **Docker Compose**.  
CI/CD настроен через **GitHub Actions (self-hosted runner)**.

---

##  Возможности

-  Проверка доступности сайта по запросу (`/check`)  
-  Автоматическое следование редиректам  
-  Сохранение истории проверок в PostgreSQL  
-  Получение истории всех проверок (`/history`)  
-  Периодическая автоматическая проверка сайтов из файла `sites.json`
-  Запуск в Docker через `docker compose`  
-  Автотесты и линтер через GitHub Actions  

---

##  Запуск проекта локально

```bash
git clone https://github.com/Sketney/site-uptime-monitor.git
cd site-uptime-monitor
docker compose up --build
```

После запуска сервис будет доступен на:  
 [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

##  Динамический список сайтов

Список сайтов для проверки хранится в файле **`sites.json`**:

```json
[
"https://google.com",
"https://github.com",
"https://fastapi.tiangolo.com"
]
```

- Изменения в `sites.json` подхватываются **без пересборки и перезапуска Docker**  
- Проверки выполняются **каждые 5 минут** автоматически  
- Результаты сохраняются в базу и доступны через `/history`  

---

## 📚 API Endpoints

| Метод | URL                        | Описание                      |
|-------|-----------------------------|-------------------------------|
| GET   | `/`                        | Проверка работы сервиса       |
| GET   | `/check?url=<ссылка>`      | Проверка сайта                |
| GET   | `/history`                 | История проверок              |

---

## 📖 Документация API

FastAPI автоматически генерирует интерактивные страницы документации:

- [Swagger UI](http://127.0.0.1:8000/docs)  
- [ReDoc](http://127.0.0.1:8000/redoc)

---

## ⚙️ CI/CD

- **Линтер**: flake8  
- **Тесты**: pytest (SQLite fallback в CI)  
- **Сборка и деплой**: self-hosted GitHub Actions runner  
- **Docker**: FastAPI + PostgreSQL через docker-compose  

---

## 🛠 Технологии

- Python 3.11  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Docker & Docker Compose  
- APScheduler  
- GitHub Actions  
