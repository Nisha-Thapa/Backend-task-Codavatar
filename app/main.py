from fastapi import FastAPI
from app.routers import virtual_phone_number
from app.db.db import create_db

app = FastAPI()

# Include the virtual phone number router
app.include_router(virtual_phone_number.router, prefix="/api", tags=["virtual phone numbers"])

# Initialize the database
@app.on_event("startup")
def on_startup():
    create_db()

# Optional: A root endpoint to check if the server is running
@app.get("/")
def read_root():
    return {"message": "Cloud Telephony Platform is Running!"}
