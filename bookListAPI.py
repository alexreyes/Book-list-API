from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from extensions import db
from models import Book

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class BookSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('title', 'link')
        
book_schema = BookSchema()
books_schema = BookSchema(many=True)


# endpoint to create new book
@app.route("/book2019", methods=["POST"])
def add_book():
    title = request.form['title']
    link = request.form['link']

    all_books = Book.query.all()
    result = books_schema.dump(all_books)

    for book in result: 
        if (book['title'] == title):
            return "Title already exists", 400
        
        if (book['link'] == link):
            return "Link already exists", 400

    new_book = Book(title, link)
    result = book_schema.dump(new_book)

    db.session.add(new_book)
    db.session.commit()

    return jsonify(result)


# endpoint to show all books
@app.route("/book2019", methods=["GET"])
def get_book():
    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    return jsonify(result)


# endpoint to get book detail by id
@app.route("/book2019/<id>", methods=["GET"])
def book_detail(id):
    book = Book.query.get(id)
    return book_schema.jsonify(book)


# endpoint to update book
@app.route("/book2019/<id>", methods=["PUT"])
def book_update(id):
    book = Book.query.get(id)
    title = request.json['title']
    link = request.json['link']

    book.link = link
    book.title = title

    db.session.commit()
    return book_schema.jsonify(book)


# endpoint to delete book
@app.route("/book2019/<id>", methods=["DELETE"])
def book_delete(id):
    book = Book.query.get(id)
    db.session.delete(book)
    db.session.commit()

    return book_schema.jsonify(book)

if __name__ == '__main__':
    app.run(debug=True)