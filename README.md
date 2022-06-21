# users_api
![posts](https://static-prod.adweek.com/wp-content/uploads/2022/06/InstagramPin3Posts.jpg.webp "astroden")
microservice in Python that provides a **RESTful API** for managing user posts

_The api integrates a third party API and an object relational model to analyze users posts_

## Exploring the cloud deployment

I have deployed it on a heroku server for the purpose of demonstration. Feel free to access it on this [link](https://users-api-dennis.herokuapp.com/ "deployed app")
The API is also documented and can be tested using a front-end client that accompanies the documentation [here](https://users-api-dennis.herokuapp.com/docs "documentation")

## How to install users_api on your local environment
1. clone the github repo and create and activate a virtual environment :
    `git clone https://github.com/DennisWanjeri/users_api.git`
    `virtualenv venv`
    `source venv/bin/activate`
2. I used python3.10 during development, however I expect versions 3.8 and above to work.
3. Run `pip install -r requirements.txt` to install all the dependencies.
4. Run `alembic upgrade head` to set up the postgres database
5. Run `uvicorn app.main:app` to run the server
6. On the browser run http://127.0.0.1:8000/docs which will reveal the documentation and the simple client-end application

## Building the docker image
Run `sudo docker build -t fastapi .`
To run the docker image `sudo docker compose -f docker-compose-dev.yml up`