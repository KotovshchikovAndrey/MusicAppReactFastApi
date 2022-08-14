import pytest_asyncio
from backend.index import app
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from backend.db import database as db
import os
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('BASE_URL')


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
            app=app,
            base_url=BASE_URL
        ) as client:
            yield client