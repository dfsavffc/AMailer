import logging

import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes import router
from app.core.config import settings

logging.basicConfig(level=logging.INFO if not settings.DEBUG else logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.APP_NAME)

app.include_router(router, prefix="/api")

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=settings.DEBUG)