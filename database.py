import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL



from settings import Settings
settings = Settings().reload()


url = URL.create(
    drivername= os.getenv('DB_DRIVER'),
    username= os.getenv('DB_USERNAME'),
    password= os.getenv('DB_PASSWORD'),
    host= os.getenv('DB_HOST'),
    database= os.getenv('DB_NAME'),
    port= os.getenv('DB_PORT')
)


engine = create_engine(url)
Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


Base.metadata.create_all(engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
