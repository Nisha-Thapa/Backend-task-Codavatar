# README
## Cloud Telephony
Service handler for Cloud Telephony application

> _<b>Swagger UI</b>_ </br>
> Available at:  <br>
> endpoint: [/ca-ct/apidoc/swagger-ui.html](http://0.0.0.0:8080/ca-ct/apidoc/swagger-ui.html) <br>


Code: [Abishek Shah](mailto:developabishek@gmail.com) <br>

&copy; **2024 CodAvatar Tech Pvt. Ltd.** All Rights Reserved. </br>
<img src="https://codavatar.com/wp-content/uploads/2023/06/codavatar-logo.svg" width="135" height="40"> <br>
<a href="https://codavatar.com/">Site</a> &nbsp; |


## How to Run the Application

### 1. Create the `.env` File

Create a file named `.env` in the root directory of your project with the following content:

<pre>
DATABASE1_URL=postgresql://postgres:postgres123@ct-postgres:5432/cloudtelephony
DB1_DRIVER_NAME=postgresql
DB1_HOST=ct-postgres
DB1_PORT=5432
DB1_USER=postgres
DB1_PASSWORD=postgres123
DB1_NAME=cloudtelephony
</pre>


### 2. Run Docker Compose

Make sure you have Docker and Docker Compose installed on your system. Navigate to the directory containing your `docker-compose.yml` file and run:
```bash
docker compose -f docker-compose.yml up --build
```


### 3. Alternatively run application without Docker

First migrate the migration file:
```bash
alembic upgrade head
```
Then run:
```bash
python main.py
```
