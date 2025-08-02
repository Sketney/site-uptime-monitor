from fastapi import FastAPI
import httpx
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Check
import json
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI(title="Site Uptime Monitor")


def scheduled_check():
    with open("sites.json") as f:
        sites = json.load(f)
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
                checked_at=datetime.now()
            )

            db.add(check)
            db.commit()
        except Exception as e:
            print(f"❌ Error checking {url}: {e}")
        finally:
            db.close()


# Создаём таблицы при старте приложения
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_check, "interval", minutes=5)
    scheduler.start()

@app.get("/")
def root():
    return {"message": "Site Uptime Monitor is running"}

# Проверка сайта
@app.get("/check")
async def check_site(url: str):
    db: Session = SessionLocal()
    try:
        start_time = datetime.now()
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
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

# История проверок
@app.get("/history")
def get_history():
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
