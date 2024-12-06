import os

from typing import Union
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI


from routes import users as user_router

from settings import Settings
settings = Settings().reload()

app = FastAPI()



app.include_router(user_router.router, prefix="/user", tags=["Users"])
