# app/main.py
from fastapi import FastAPI
import httpx
from datetime import datetime

app = FastAPI(title="Site Uptime Monitor")


@app.get("/")
def root():
    return {"message": "Site Uptime Monitor is running"}


@app.get("/check")
async def check_site(url: str):
    try:
        start_time = datetime.now()
        async with httpx.AsyncClient(timeout=5, follow_redirects=True) as client:
            response = await client.get(url)
        response_time = (datetime.now() - start_time).total_seconds()
        return {
            "url": url,
            "final_url": str(response.url),
            "status_code": response.status_code,
            "response_time": response_time,
            "checked_at": datetime.now()
        }
    except Exception as e:
        return {"url": url, "error": str(e), "checked_at": datetime.now()}

