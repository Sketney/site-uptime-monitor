from fastapi import FastAPI
import httpx
from datetime import datetime
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Check

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Site Uptime Monitor")


@app.get("/")
def root():
    return {"message": "Site Uptime Monitor is running"}


@app.get("/check")
async def check_site(url: str):
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
