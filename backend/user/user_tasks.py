from user.user_celery import app
import asyncio
from user.user_models import JwtToken as token_model
from db import database


async def _clear_expired_token(token_value: str):
    await database.connect()
    
    query = f"DELETE FROM {token_model.__table__} WHERE refresh_token = '{token_value}'"
    await database.execute(query=query)
    
@app.task
def clear_expired_token_task(token_value: str):
    asyncio.run(
        _clear_expired_token(
            token_value=token_value
        )
    )

    