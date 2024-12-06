from fastapi import FastAPI
from app.api import routes
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=" Cloud Telephony API Development (Scoped Version)",
    description="APIs will allow users to manage virtual phone numbers by creating and retrieving them",
    version="1.0.0",
)

app.include_router(routes.router)


@app.get("/", tags=["root"])
async def read_root():
    return {"message": "Welcome to the API!"}
