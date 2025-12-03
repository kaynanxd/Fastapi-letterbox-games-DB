import asyncio
import sys
from http import HTTPStatus

from fastapi import FastAPI

from app.routers import auth, watchlist, users
from app.schemas.common import Message

from fastapi.staticfiles import StaticFiles

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



app = FastAPI()

app.mount("/media", StaticFiles(directory="media"), name="media")

app.include_router(users.router)
app.include_router(watchlist.router)
app.include_router(auth.router)


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}