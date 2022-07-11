# **Weather API**

### **Table of contents:**

- Installation guide
	- Windows
	- Linux
- API Endpoints
	- City Weather
	- User
	- Token authorization
	- Swagger
- Celery
	- Run scheduled tasks
	- Run basic tasks
	- Add new scheduled tasks
- Technical decisions

## **Installation guide**
 
### **Windows:**
 
1. **Install** [Python 3.8](https://www.python.org/ftp/python/3.8.8/python-3.8.8rc1-amd64.exe), [PostgreSQL](https://www.enterprisedb.com/postgresql-tutorial-resources-training?uuid=db55e32d-e9f0-4d7c-9aef-b17d01210704&campaignId=7012J000001NhszQAC), [Erlang for rabbitmq](https://github.com/erlang/otp/releases/download/OTP-25.0.2/otp_win64_25.0.2.exe), [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.10.5/rabbitmq-server-3.10.5.exe)
   - ***Start RabbitMQ***:
	  - **Navigate** to `C:\Program Files\RabbitMQ Server\rabbitmq_server-3.10.5\sbin`
	  - **Start** `rabbitmq-server.bat` as **Administrator**

2. If you haven't already **clone** the repository and `cd` into it
	```bash
	git clone https://github.com/antonarnaudov/weather_api.git
	cd weather_api
	```
	 
3. **Create** local **database** named `weather-api-db` using pgAdmin or SQL Shell (psql)
<br />***NOTE:*** Make sure you set proper credentials in `DATABASE` settings

4. **Create** `venv` by running:
	```bash
	python -m venv venv
	```
 
5. **Activate** `venv` in:
	- ***cmd*** by running: 
		```cmd
		call venv/scripts/activate
		```
	- ***Powershell*** by running:
		```powershell
		& venv/scripts/activate
		``` 
 
6. **Install** all dependencies by running:
	```bash
	pip install -r requirements.txt
	```

7. **Run** migrations with:
	```bash
	python manage.py migrate
	```
 
8. Try **starting** the app with:
	```bash 
	python manage.py runserver
	```

### **Linux:**
 
1. **Install** [PostgreSQL](https://www.postgresql.org/download/)
	<br />**Python3.8:**
	```bash 
	sudo apt-get install python3.8
	```
	**RabbitMQ:** 
	```bash
	sudo apt-get install rabbitmq-server
	sudo systemctl enable rabbitmq-server
	sudo systemctl start rabbitmq-server
	```
	Optional (to make sure it works): `systemctl status rabbitmq-server`
 
2. If you haven't already **clone** the repository and `cd` into it
	```bash
	git clone https://github.com/antonarnaudov/weather_api.git
	cd weather_api
	```
	 
3. **Create** local **database** named `weather-api-db` using pgAdmin or SQL Shell (psql)
<br />***NOTE:*** Make sure you set proper credentials in `DATABASE` settings

4. **Create** `venv` by running:
	```bash
	python3 -m venv venv
	```
 
5. **Activate** `venv` by running 
	```bash
	source venv/bin/activate
	```
 
6. **Install** all dependencies with:
	```bash
	pip install -r requirements.txt
	```
 
7. **Run** migrations with:
	```bash
	python3 manage.py migrate
	```
 
8.  Try **starting** the app with:
	```bash 
	python3 manage.py runserver
	```

## **API Endpoints**

### **City Weather**

> Provides access to weather data for all cities

**Read Only:** `api/cityweather/`

**Detailed:** `api/cityweather/{id}/`
<br/>
![search](https://img.icons8.com/officexs/16/1A1A1A/search.png) **Search by city:** `api/cityweather/?city=sofia`


### **User**

> Provides endpoints for user profile management

**CRUD:** `api/auth/user/`
```json
{
  "id": 1,
  "extended": {
    "id": 1,
    "phone": "0888666754"
  },
  "last_login": null,
  "is_superuser": true,
  "username": "admin",
  "first_name": "Admin",
  "last_name": "Adminov",
  "email": "admin@cityweather.com",
  "is_staff": true,
  "is_active": true,
  "date_joined": "2022-07-09T18:53:58.243512Z",
  "groups": [],
  "user_permissions": []
}
```
![enter image description here](https://img.icons8.com/officexs/16/1A1A1A/search.png) **Search:** `api/auth/user/?search=admin`
**Search fields:** `first_name`, `last_name`, `email`,  `username`

***Register Users on POST***<br/>
**Required fields on POST:** `username`, `password`, `password2`, `email`

### **Token authorization**

> Takes a set of user credentials and returns an access and refresh JSON web  
token pair to prove the authentication of those credentials.

#### Get token
**POST:** `api/auth/login/`<br/>
***Expects:*** 
```json
{
  "username": "admin",
  "password": "1234"
}
```
***Returns:*** 
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NzY1NTA2NywiaWF0IjoxNjU3NTY4NjY3LCJqdGkiOiIxOTg4NWE1OGIzNTk0NzJiYjI2NmNjY2FjZGZmN2JkNyIsInVzZXJfaWQiOjF9.7zKhghN_UgQQW_7QnjfMckUOfaE3txwYnoXvEVoZQ8E",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU3NTY4OTY3LCJpYXQiOjE2NTc1Njg2NjcsImp0aSI6ImVjZTQ5YjdiZTdkNzQ2Y2NhZjlhNWEwZTNlOWQ4MjhjIiwidXNlcl9pZCI6MX0.HqXlOh1RrOxocD2kmpUJy2cqH1lZagtwCl-iJSsm4ro"
}
```
#### **Refresh token**
**POST:** `api/auth/refresh/`<br/>
***Expects:***
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NzY1NTA2NywiaWF0IjoxNjU3NTY4NjY3LCJqdGkiOiIxOTg4NWE1OGIzNTk0NzJiYjI2NmNjY2FjZGZmN2JkNyIsInVzZXJfaWQiOjF9.7zKhghN_UgQQW_7QnjfMckUOfaE3txwYnoXvEVoZQ8E"
}
```
***Returns:***
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU3NTY5MTIwLCJpYXQiOjE2NTc1Njg2NjcsImp0aSI6IjRlZThkZTk5ZDYzYzRiNjdiODAyYmU3ODhlZGY0ZWFjIiwidXNlcl9pZCI6MX0.6i0qPK0KLjRwFMkoO6R-s5IrWBImT5Rt86Xu6GntQc8"
}
```

#### **IMPORTANT:**

To use the access token in request, simply add it to request headers as: `Authorization: Bearer ${access}`

Token Lifespan:
- Access token lifespan is 5 minutes
- Refresh token lifespan is 1 day
- To retain an ongoing session you should refresh the access token on every request

### **Swagger**

> Auto-generated documentation for all accessible endpoints

**GET:** `api/swagger/`

## **Celery Tasks**

> Make sure you have started the RabbitMQ Server

**NOTE:** You can skip those steps if you've already done them

On **Linux** you should execute the following commands:
```bash
sudo systemctl enable rabbitmq-server
sudo systemctl start rabbitmq-server
```
On **Windows** you should:
	  - **Navigate** to `C:\Program Files\RabbitMQ Server\rabbitmq_server-3.10.5\sbin`
	  - **Start** `rabbitmq-server.bat` as **Administrator**

### **Run scheduled tasks:**
Open any terminal and execute this line to start the celery workers:
<br/>***For Windows:***
```bash
celery -A weather_api worker -l info --pool=solo
```
***For Linux:***
```bash
celery -A weather_api worker -l info
```

In a separate terminal run this line to start the celery beat and all scheduled tasks:
```bash
celery -A weather_api beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
```

### **Run basic tasks:**
Open any terminal and execute this line to start the celery workers:
<br />***For Windows:***
```bash
celery -A weather_api worker -l info --pool=solo
```
***For Linux:***
```bash
celery -A weather_api worker -l info
```

### **Add new scheduled tasks:**
1. Create `@app.task` decorated function in any file or app
	- Import `app` from `weather_api.celery`
2. Open weather_api > celery.py and register your worker inside app.conf.beat_schedule following this structure
```js
"example_worker_runs_every_minute": {
	"task": "app.file.worker_function",
	"schedule": 60.0 # schedule expects seconds
}
```

## **Technical decisions**
1. I used RabbitMQ instead of Redis for message broker because I aimed to make the project executable on both Windows and Unix based OS. Redis requires a WSL to run under windows and RabbitMQ can work directly under it, although it requires to manually start the server.

2. I used a custom filter instead of overriding the list method for the search by city, thus keeping the ViewSet super clean and simple

3. I used JsonFiled for storing the third party api data, which worked really nice with the Django ORM, allowing me to tap into the nested fields as if they were written in the model

4. I used created_at/updated_at DateTime fields to keep track of time ;-D, so i know when to refresh the data

5. I extended the user model (although it wasn't necessary) as a matter of good practice, because its nightmare to do it later in the development process, when the app expands

6. I moved all non-weather specific functionality in app named core, and all utility functions in core > utils

7. I added a custom mixin which allows me to dynamically change the serializer, based on the request type

8. The default pagination class is overridden, so it utilizes size parameter, for dynamic single page pagination

9. I added a custom exception handler, to minimize the chance for Server Error 500 response

10. All Open Weather Map API credentials are set as settings 

11. Added a blank page on base rout so it does not throw errors

12. I used PR-s for this projects and did not delete the branches so you can track the full development history

13. I used WritableNestedSerializers to create Extended objects from the Users serializer

14. I provided console logging on the celery task which logs the time of execution and the next time of execution
