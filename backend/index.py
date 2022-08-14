import sys
import os

sys.path.append(os.path.join(sys.path[0], 'backend'))

from fastapi import FastAPI, Request
from user import user_controllers
from music import music_controllers
from db import database
from error.exception_errors import ApiError
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(__file__)
MEDIA_DIR = os.path.join(BASE_DIR, 'media')

app = FastAPI()

app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")
app.include_router(music_controllers.router)
app.include_router(user_controllers.router)


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()


@app.middleware('http')
async def exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        if isinstance(exc, ApiError):
            return JSONResponse(
                status_code=exc.status,
                content={
                    'message': exc.msg,
                    'errors': exc.error_list
                }
            )
        
        return JSONResponse(
                status_code=500,
                content={'message': 'Непредвиденная ошибка сервера!'}
            )
