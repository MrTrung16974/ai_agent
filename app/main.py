from fastapi import FastAPI

from .api.routes import router as items_router
from .core.config import get_settings
from .db import engine
from .models import Base

settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(items_router)


@app.on_event("startup")
async def on_startup() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health", tags=["health"])
async def health_check() -> dict[str, str]:
    return {"status": "ok"}
