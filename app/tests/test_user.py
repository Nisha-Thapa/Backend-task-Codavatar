import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import User, VirtualPhoneNumber
from app.db import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import bcrypt

# Load environment variables from .env file
load_dotenv()

# Use the DATABASE_URL environment variable or default to SQLite for testing
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost/testdb")

# Setup for the test database (using a PostgreSQL database for tests)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Test database fixture
@pytest.fixture(scope="module")
def db():
    # Create the tables in the test database
    User.metadata.create_all(bind=engine)
    VirtualPhoneNumber.metadata.create_all(bind=engine)
    db_session = SessionLocal()
    yield db_session
    db_session.close()
    
    # Drop the tables after tests run
    User.metadata.drop_all(bind=engine)
    VirtualPhoneNumber.metadata.drop_all(bind=engine)

# Create a TestClient instance to interact with the FastAPI app
@pytest.fixture
def client():
    return TestClient(app)

# Test case for creating a user
def test_create_user(client, db):
    # Prepare test data
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }

    # Send a POST request to create the user
    response = client.post("/api/users/", json=user_data)

    # Assert response status code is 200 (success)
    assert response.status_code == 200

    # Assert response contains the user data (excluding password)
    response_data = response.json()
    assert "id" in response_data
    assert response_data["name"] == user_data["name"]
    assert response_data["email"] == user_data["email"]

    # Check if the user is actually stored in the database
    db_user = db.query(User).filter(User.email == user_data["email"]).first()
    assert db_user is not None
    assert db_user.name == user_data["name"]
    assert db_user.email == user_data["email"]

    # Ensure that the password is hashed
    assert db_user.password != user_data["password"]
    # Check if the plaintext password matches the hashed password
    assert bcrypt.checkpw(user_data["password"].encode("utf-8"), db_user.password.encode("utf-8"))

    # Delete the created user from the database
    db.delete(db_user)
    db.commit()

# Test case for creating a user with an existing email
def test_create_user_with_existing_email(client, db):
    # First, create a user
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "testpassword"
    }
    client.post("/api/users/", json=user_data)

    # Try creating another user with the same email
    response = client.post("/api/users/", json=user_data)

    # Assert response status code is 400 (email already registered)
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}

    # Delete the created user from the database
    db_user = db.query(User).filter(User.email == user_data["email"]).first()
    db.delete(db_user)
    db.commit()

# Test case for creating a new virtual phone number for a user
def test_create_virtual_phone_number(client, db):
    # Create a user first
    user_data = {
        "name": "Test User",
        "email": "test1@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    user_id = response_data["id"]

    # Prepare test data for the virtual phone number
    phone_number_data = {
        "user_id": user_id,
        "number": "1234567890"  # Example phone number
    }

    # Send a POST request to create the virtual phone number
    response = client.post("/api/virtual-phone-numbers", json=phone_number_data)

    # Assert response status code is 200 (success)
    assert response.status_code == 200

    # Assert response contains the phone number data
    response_data = response.json()
    assert "id" in response_data
    assert response_data["number"] == phone_number_data["number"]
    assert response_data["user_id"] == phone_number_data["user_id"]

    # Check if the virtual phone number is actually stored in the database
    db_phone_number = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.number == phone_number_data["number"]).first()
    assert db_phone_number is not None
    assert db_phone_number.number == phone_number_data["number"]
    assert db_phone_number.user_id == phone_number_data["user_id"]

    # Delete the virtual phone number from the database
    db.delete(db_phone_number)
    db.commit()

    # Delete the user from the database
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()

# Test case for creating a virtual phone number with an already existing number
def test_create_virtual_phone_number_with_existing_number(client, db):
    # Create a user first
    user_data = {
        "name": "Test User",
        "email": "test1@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    user_id = response_data["id"]

    # Prepare test data for the virtual phone number
    phone_number_data = {
        "user_id": user_id,
        "number": "1234567890"  # Example phone number
    }

    # Create the first virtual phone number
    response = client.post("/api/virtual-phone-numbers", json=phone_number_data)
    assert response.status_code == 200

    # Try to create the same virtual phone number again
    response = client.post("/api/virtual-phone-numbers", json=phone_number_data)

    # Assert response status code is 400 (phone number already in use)
    assert response.status_code == 400
    assert response.json() == {"detail": "Phone number already in use"}

    # Delete the virtual phone number from the database
    db_phone_number = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.number == phone_number_data["number"]).first()
    db.delete(db_phone_number)
    db.commit()

    # Delete the user from the database
    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()

# Test case for retrieving virtual phone numbers owned by a user
def test_get_virtual_phone_numbers(client, db):
    # Create a user first
    user_data = {
        "name": "Test User",
        "email": "test2@example.com",
        "password": "testpassword"
    }
    response = client.post("/api/users/", json=user_data)
    assert response.status_code == 200
    response_data = response.json()
    user_id = response_data["id"]

    # Add some virtual phone numbers for this user
    phone_numbers_data = [
        {"user_id": user_id, "number": "1234567890"},
        {"user_id": user_id, "number": "0987654321"}
    ]

    # Create the first phone number
    response = client.post("/api/virtual-phone-numbers", json=phone_numbers_data[0])
    assert response.status_code == 200

    # Create the second phone number
    response = client.post("/api/virtual-phone-numbers", json=phone_numbers_data[1])
    assert response.status_code == 200

    # Send a GET request to retrieve virtual phone numbers for the user
    response = client.get(f"/api/virtual-phone-numbers/{user_id}")
    
    # Assert response status code is 200 (success)
    assert response.status_code == 200
    
    # Assert that the response contains the correct list of virtual phone numbers
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 2  # We created 2 phone numbers
    
    # Verify the phone numbers in the response match the ones created
    assert any(phone["number"] == "1234567890" for phone in response_data)
    assert any(phone["number"] == "0987654321" for phone in response_data)

    # Clean up by deleting the created virtual phone numbers and the user
    for phone in response_data:
        db_phone_number = db.query(VirtualPhoneNumber).filter(VirtualPhoneNumber.id == phone["id"]).first()
        db.delete(db_phone_number)
        db.commit()

    db_user = db.query(User).filter(User.id == user_id).first()
    db.delete(db_user)
    db.commit()
