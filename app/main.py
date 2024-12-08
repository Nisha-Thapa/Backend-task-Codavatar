from fastapi import FastAPI
from .db import Base, engine
from .routers import users, phone_numbers

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(phone_numbers.router, prefix="/api/phone-numbers", tags=["Phone Numbers"])
