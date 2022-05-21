from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

BASE = "https://jsonplaceholder.typicode.com"
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"{self.id} - {self.userId}"

class Posts(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(400), nullable=False)

    def __repr__(self):
        return f"{self.user_id} - {self.title} - {self.body}"
    

@app.route('/post')
def index():
    return 'Hello!'  

