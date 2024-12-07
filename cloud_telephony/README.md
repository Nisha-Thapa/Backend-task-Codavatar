# 🚀 Cloud Telephony API

A simplified Cloud Telephony API to manage virtual phone numbers, with user authentication and token-based security using JWT. This project uses FastAPI, SQLAlchemy, SQLite, and Docker for deployment.

---

## 📖 Overview

This project provides the following features:

- **User Registration and Authentication**: Securely register and log in users using JWT-based authentication.
- **Virtual Phone Number Management**: Allow users to create virtual phone numbers linked to their account.
- **Secure Routes with JWT Authentication**: Only authenticated users can access certain endpoints.

---

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (via SQLAlchemy ORM)
- **Authentication**: JWT (JSON Web Tokens)
- **Docker**: Dockerize the application for deployment
- **Tools**: Python-dotenv for environment variable management
- **Package Manager**: `pip`

---

## 📂 Folder Structure

```
cloud_telephony/
│
├── app/
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth_utils.py
│   ├── auth_dependency.py
│   └── routes/
│       ├── phone_routes.py
│       └── auth_routes.py
│
├── docker/
│   └── Dockerfile
│
├── docker-compose.yml
│
├── .env
│
├── requirements.txt
│
└── README.md
```

---

## 🏆 Features

### 🔹 **User Registration**

- **Endpoint**: `/auth/register`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

---

### 🔹 **User Login**

- **Endpoint**: `/auth/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "string",
    "token_type": "bearer"
  }
  ```

---

### 🔹 **Create Virtual Phone Number**

- **Endpoint**: `/phone_numbers`
- **Method**: `POST`
- **Headers**:
  ```
  Authorization: Bearer <access_token>
  ```
- **Request Body**:
  ```json
  {
    "phone_number": "+1234567890"
  }
  ```
- **Response**:
  ```json
  {
    "id": 1,
    "phone_number": "+1234567890",
    "user_id": 1
  }
  ```

---

## 🛠️ Installation

### Clone the repository
```bash
git clone https://github.com/yourusername/cloud_telephony.git
cd cloud_telephony
```

### Set up the environment (Optional for this project as I am using docker)
1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the virtual environment:

- **Linux/Mac**:
```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🐳 Running with Docker (User Docker Instead of above Set up the environment)

The app is dockerized using **Docker Compose**.

### Start the services:

```bash
docker-compose up --build
```

The application should now be running at:

- **http://localhost:8000**

You can test the API via the Swagger docs available at:

- **http://localhost:8000/docs**

---

## 💡 Environment Variables

The `.env` file is required for configuration.

### Create a `.env` file:
```plaintext
SECRET_KEY=jwt_secret_key_yours
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Generate a JWT secret securely**:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the generated token as the value of `SECRET_KEY`.

---

## 🧪 Testing the Application

The FastAPI documentation is automatically generated and can be found at:

- **http://localhost:8000/docs**

Test endpoints such as:
1. `/auth/register` to register a new user.
2. `/auth/login` to log in and retrieve a JWT token.
3. `/phone_numbers` to create a new virtual phone number (use the token in the `Authorization` header).

---

## 💾 Database Schema

The SQLite database schema includes the following models:

### **User**

| Column           | Type       | Description                       |
|------------------|------------|-----------------------------------|
| `id`             | Integer    | Primary Key                      |
| `username`       | String     | Unique username                  |
| `hashed_password` | String    | Hashed password                  |

---

### **VirtualPhoneNumber**

| Column           | Type       | Description                       |
|------------------|------------|-----------------------------------|
| `id`             | Integer    | Primary Key                      |
| `phone_number`   | String     | Virtual phone number             |
| `user_id`        | Integer    | Foreign key linking user ownership |

---

## 🔧 Dependencies

### Required Python Packages
```plaintext
fastapi
uvicorn
sqlalchemy
pydantic
python-jose
passlib[bcrypt]
python-dotenv
```

---

## 🏆 Acknowledgments

- **FastAPI Documentation**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **SQLAlchemy ORM**: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
- **Docker Documentation**: [https://www.docker.com/](https://www.docker.com/)

---