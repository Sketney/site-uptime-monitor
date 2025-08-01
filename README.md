# Site Uptime Monitor

Учебный DevOps-проект для портфолио.  
Приложение проверяет доступность сайтов, сохраняет результаты в базу данных, 
отображает историю проверок на веб-странице и отправляет уведомления в Telegram при падении сайта.

## 🚀 Технологический стек
- **Backend**: Python 3.11 + FastAPI
- **Database**: PostgreSQL
- **Infrastructure**: Docker, docker-compose
- **CI/CD**: GitHub Actions
- **Monitoring**: Prometheus + Grafana
- **Alerting**: Telegram Bot API
- **IaC**: Terraform
- **Automation**: Ansible

## 🔧 Функциональность
- Проверка доступности сайтов по расписанию
- Хранение результатов в базе PostgreSQL
- Просмотр истории через веб-интерфейс
- Метрики (время ответа, код состояния)
- Графики доступности и времени ответа в Grafana
- Уведомления в Telegram о падениях сайтов

## 📂 Структура проекта
site-uptime-monitor/
│── app/ # Backend (FastAPI)
│── infra/ # Инфраструктура (Docker, Terraform, Ansible)
│── tests/ # Тесты (pytest)
│── .github/workflows/ # CI/CD (GitHub Actions)
│── README.md

## ⚡ CI/CD
- Автоматическая проверка кода (flake8, pytest)
- Сборка Docker-образа
- Деплой на сервер через Ansible и Terraform

## 📊 Мониторинг
- Prometheus собирает метрики
- Grafana визуализирует дашборды
- Telegram Bot отправляет уведомления о сбоях
