import os

from typing import Union
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI


from routes import users as user_router
from routes import phone as phone_router

from settings import Settings
settings = Settings().reload()

app = FastAPI()



app.include_router(user_router.router, prefix="/user", tags=["Users"])
app.include_router(phone_router.router, prefix="/phone", tags=["Phone"])
