from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from models import Book

app = Flask(__name__)
db = SQLAlchemy(app)