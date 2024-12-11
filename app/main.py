from fastapi import FastAPI
from app.routers import virtual_phone_number,user
from app.db import create_db

app = FastAPI()

# Include router
app.include_router(virtual_phone_number.router, prefix="/api", tags=["virtual phone numbers"])
app.include_router(user.router,prefix="/api",tags=["users"])


# Initialize the database
@app.on_event("startup")
def on_startup():
    create_db()

# A root endpoint to check if the server is running
@app.get("/")
def read_root():
    return {"message": "Cloud Telephony Platform is Running!"}
