import os
from logging import Logger
from contextlib import asynccontextmanager

import redis
from fastapi import FastAPI

from backend.app.routers import auth_router
from backend.app.core.config import settings
from backend.app.core.database import Base, async_engine

logger = Logger

redis_client = redis.Redis(
    host=os.getenv("DB_HOST", "redis"),
    port=int(os.getenv("DB_PORT", 6379)),
    decode_responses=True
)

visits = redis_client.incr("visits")
logger.info(f" Hello from Docker.\nredis_visits: {visits}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Check for URL DB: {settings.database_url}")

    async with async_engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)
    logger.info("Connection to database established...")
    yield
    await async_engine.dispose()

app = FastAPI(title="Welcome to FastAPI Shop", lifespan=lifespan)

app.include_router(auth_router.router)
