from fastapi import FastAPI
# from .routers import phone_numbers
# from .database import engine
# from .models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(phone_numbers.router, prefix="/api/v1")
