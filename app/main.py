from api.routers import main_router
from core.config import settings
from core.init_db import create_first_superuser
from fastapi import FastAPI

app = FastAPI(title=settings.app_title)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    await create_first_superuser()