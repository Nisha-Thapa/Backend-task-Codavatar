from fastapi import FastAPI
from app.routers import phone_numbers, users
from .database import engine
from .models import Base

app = FastAPI()

# Startup event to initialize the database
@app.on_event("startup")
async def startup():
    # Create database tables if they don't exist yet
    Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Please refer to /docs for API documentation"}

# Including routers for phone numbers and users
app.include_router(phone_numbers.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
