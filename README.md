# 🌐 Site Uptime Monitor

![CI/CD](https://github.com/Sketney/site-uptime-monitor/actions/workflows/ci-cd.yml/badge.svg)

**Site Uptime Monitor** — сервис для мониторинга доступности веб-сайтов с сохранением истории и метрик.  
Реализован на **FastAPI**, использует **PostgreSQL**, **Prometheus** и **Grafana**.  
CI/CD настроен через **GitHub Actions (self-hosted runner)**.

---

## ✨ Возможности

- ✅ Проверка доступности сайта по запросу (`/check`)  
- ✅ Автоматическое следование редиректам  
- ✅ Сохранение истории проверок в PostgreSQL  
- ✅ Получение истории всех проверок (`/history`)  
- ✅ **Периодическая автоматическая проверка сайтов из файла `sites.json`**  
- ✅ Метрики на `/metrics` для Prometheus  
- ✅ Дашборд в Grafana (время ответа, количество успешных/неудачных проверок, распределение кодов HTTP)  
- ✅ Запуск в Docker через `docker compose`  
- ✅ Автотесты и линтер через GitHub Actions  

---

## 🚀 Запуск проекта локально

```bash
git clone https://github.com/Sketney/site-uptime-monitor.git
cd site-uptime-monitor
docker compose up --build
```

После запуска сервисы будут доступны:

- API: [http://127.0.0.1:8000](http://127.0.0.1:8000)  
- Prometheus: [http://127.0.0.1:9090](http://127.0.0.1:9090)  
- Grafana: [http://127.0.0.1:3000](http://127.0.0.1:3000) (логин/пароль: `admin/admin`)  

---

## 🔍 Динамический список сайтов

Список сайтов для проверки хранится в файле **`sites.json`**:

```json
[
"https://google.com",
"https://github.com",
"https://fastapi.tiangolo.com"
]
```

- Изменения в `sites.json` подхватываются **без пересборки и перезапуска Docker**  
- Интервал проверки задаётся в коде (по умолчанию 1 минута)  
- Результаты сохраняются в базу и доступны через `/history`  

---

## 📚 API Endpoints

| Метод | URL                        | Описание                      |
|-------|-----------------------------|-------------------------------|
| GET   | `/`                        | Проверка работы сервиса       |
| GET   | `/check?url=<ссылка>`      | Проверка сайта                |
| GET   | `/history`                 | История проверок              |

---

## 📊 Grafana Dashboard

В дашборде отображаются:
- 📈 **Response Time per Site** — график времени отклика для каждого сайта  
- ✅ **Total Successful Checks** — количество успешных проверок  
- ❌ **Total Failed Checks** — количество ошибок  
- 🍩 **HTTP Status Codes** — распределение кодов ответа  
- 📋 **Последние результаты проверки** — таблица с историей  

---

## ⚙️ CI/CD

- **Линтер**: flake8  
- **Тесты**: pytest (SQLite fallback в CI)  
- **Сборка и деплой**: self-hosted GitHub Actions runner  
- **Docker**: FastAPI + PostgreSQL + Prometheus + Grafana  

---

## 🛠 Технологии

- Python 3.11  
- FastAPI  
- SQLAlchemy  
- PostgreSQL  
- Prometheus  
- Grafana  
- Docker & Docker Compose  
- APScheduler  
- GitHub Actions  
