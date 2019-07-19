# Python_RESTFul_API_Service_App
##### REST API App based on Python Flask framework with JWT Authentiaction

### Part of [Laravel Base API microservices project](https://github.com/Maksim1990/Laravel_Base_API_project)
- [CHECK ALSO SWAGGER DOCS OF DEMO APP](http://185.177.59.147:5001/api/docs/)

---
#### _Microservice for storing user's notes_
**FOLLOWING TECHNOLOGIES ARE USED**
- Python 3.7, Flask framework
- MySQL, MongoDB
---


**HOT TO INSTALL APP**
--

* *Start app and build required Docker containers:*

        docker-compose up -d

* *Copy ``.env`` environment config file and set all required settings in it:*

        docker exec -it flask_api cp .env.dist .env

* *Run all required migrations (**won't be overwriten if already exist**):*

        curl -X GET http://localhost:5000/api/v1/migrate -H 'Content-Type: application/json'

App is available on ``5000`` port
--
    http://127.0.0.1:5000

#### Swagger API documentation will be available by following [URL](http://127.0.0.1:5000/api/docs/)
