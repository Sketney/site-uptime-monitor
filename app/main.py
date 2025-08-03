from fastapi import FastAPI
import httpx
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Check
import json
from apscheduler.schedulers.background import BackgroundScheduler
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Site Uptime Monitor")

# Подключаем Prometheus метрики
Instrumentator().instrument(app).expose(app)


def scheduled_check():
    try:
        with open("/app/sites.json") as f:
            sites = json.load(f)
    except Exception as e:
        print(f"❌ Не удалось открыть sites.json: {e}")
        return

    for url in sites:
        db: Session = SessionLocal()
        try:
            start_time = datetime.now()
            with httpx.Client(timeout=5, follow_redirects=True) as client:
                response = client.get(url)
            response_time = (datetime.now() - start_time).total_seconds()

            check = Check(
                url=url,
                final_url=str(response.url),
                status_code=response.status_code,
                response_time=response_time,
                checked_at=datetime.now(),
                error=None
            )
            db.add(check)
            db.commit()

        except Exception as e:
            print(f"❌ Ошибка при проверке {url}: {e}")
            check = Check(
                url=url,
                final_url=None,
                status_code=None,
                response_time=None,
                checked_at=datetime.now(),
                error=str(e)  # сохраняем текст ошибки
            )
            db.add(check)
            db.commit()
        finally:
            db.close()


@app.on_event("startup")
def on_startup():
    """Инициализация базы и запуск планировщика"""
    Base.metadata.create_all(bind=engine)
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_check, "interval", minutes=1)
    scheduler.start()
    print("🚀 Site Uptime Monitor запущен!")


@app.get("/")
def root():
    return {"message": "Site Uptime Monitor is running"}


@app.get("/check")
async def check_site(url: str):
    """Проверка одного сайта по запросу"""
    db: Session = SessionLocal()
    try:
        start_time = datetime.now()
        async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
            response = await client.get(url)
        response_time = (datetime.now() - start_time).total_seconds()

        check = Check(
            url=url,
            final_url=str(response.url),
            status_code=response.status_code,
            response_time=response_time,
            checked_at=datetime.now()
        )

        db.add(check)
        db.commit()
        db.refresh(check)

        return {
            "url": check.url,
            "final_url": check.final_url,
            "status_code": check.status_code,
            "response_time": check.response_time,
            "checked_at": check.checked_at
        }
    except Exception as e:
        return {"url": url, "error": str(e), "checked_at": datetime.now()}
    finally:
        db.close()


@app.get("/history")
def get_history():
    """Получение истории всех проверок"""
    db: Session = SessionLocal()
    try:
        checks = db.query(Check).order_by(Check.checked_at.desc()).all()
        return [
            {
                "id": check.id,
                "url": check.url,
                "final_url": check.final_url,
                "status_code": check.status_code,
                "response_time": check.response_time,
                "checked_at": check.checked_at
            }
            for check in checks
        ]
    finally:
        db.close()
