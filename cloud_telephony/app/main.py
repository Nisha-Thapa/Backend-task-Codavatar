import sys
import os

# Ensure base directory is in the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes.phone_routes import phone_router
from routes.auth_routes import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(phone_router)
app.include_router(router)
