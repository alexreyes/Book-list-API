from flask import Flask, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from models import Book
import os

app = Flask(__name__)

# config
app.config.from_object(os.environ['APP_SETTINGS'])
print(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

@app.route("/bookList")
def bookList(): 
    posts = db.session.query(Book).all()
    lines = posts

    response = jsonify(lines)
    response.headers.add('Access-Control-Allow-Origin', '*')
    
    # file.close()

    return response