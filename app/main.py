from fastapi import FastAPI
from app.routers import phone_numbers, users
from .database import engine
from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Please refer to /docs for API documentation"}

app.include_router(phone_numbers.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
