# users_api
microservice in Python that provides a RESTful API for managing user posts

The api integrates a third party API and an object relational model to analyze posts.

# exploring the cloud deployment

I have deployed it on a heroku server for the purpose of demonstration. Feel free to access it on this link https://users-api-dennis.herokuapp.com/
The API is also documented and can be tested using a front-end client that accompanies the documentation on https://users-api-dennis.herokuapp.com/docs

# How to install users_api on your local environment
1. clone the github repo
2. I used python3.10 during development, however I expect versions 3.8 and above to work.
3. Run pip install -r requirements.txt to install all the dependencies.
4. Run alembic upgrade head to set up the postgres database
5. Run uvicorn app.main:app to run the server
6. Run http://127.0.0.1:8000/docs which will reveal the documentation and the simple client-end application