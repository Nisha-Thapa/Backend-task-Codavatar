# Project setup

#### Clone the repo
```bash
git clone https://github.com/jATM0S/Associate-Backend-task-Codavatar
```
#### Create virtual environment 
```bash
python -m venv venv
```

#### Activate virtual environment
windows
```bash
.venv\Scripts\activate
```
powershell
```bash
.\venv\Scripts\Activate.ps1
```
linux/mac
```bash
source venv/bin/activate
```
#### Go to the app directory 
```bash
cd app
```

#### Install dependencies
```bash
python install -r requirements.txt
```
#### Create database
In psql shell
```bash
CREATE DATABASE codavatar_task;
GRANT ALL PRIVILEGES ON DATABASE codavatar_task TO <YOUR LOGIN ROLE NAME>;
```
or 
Use pgAdmin to create database and set the owner(user).

Do toggle the login privledge in to the Login/Group Roles user

#### Make .env  
Create .env file in app similar to .env.example. Put the necessary parameters like DB_USER, DB_PASSWORD...

#### Migrate 
```bash
python manage.py migrate
```
#### Create superuser
```bash
python manage.py createsuperuser
```
#### Run the code
```bash
python manage.py runserver
```

## Endpoints
|Activity|Endpoints|Req type|
|---|---|---|
|Create user |127.0.0.1:8000/user/signup|POST|
|Login |127.0.0.1:8000/user/login |POST|
| Create virtual numbers| 127.0.0.1:8000/virtualno/create|POST|
| Show virtual numbers| 127.0.0.1:8000/virtualno/show|GET|
### Request body example 
Create user:
{
    "username":"Krisp",
    "email":"crispy@gmail.com",
    "password":"crunchy",
    "phone_no":"9888382836"
}

LogIn:
{
    "email":"crispy@gmail.com",
    "password":"crunchy"
}

### For virtual phone no 
Token will be given by the login and signup response.
Custom header has to be made for virtual no apis with key=Authentication and value Token <token>.

Create virtual no:
{
    "phone_no":"958382827",
    "username":"Krisp"
}

Show virtual no:
{
    "username":"Krisp"
}