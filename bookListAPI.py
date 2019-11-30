from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from goodreadsScrape import get_books
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config.from_pyfile('settings.py')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    link = db.Column(db.String(120), unique=True)

    def __init__(self, title, link):
        self.title = title
        self.link = link


class BookSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('title', 'link')


book_schema = BookSchema()
books_schema = BookSchema(many=True)

@app.route('/')
def index(): 
    return "This is my book API. By Alex Reyes. For use in www.alexreyes.xyz"

# endpoint to create new book
@app.route("/book2019", methods=["POST"])
def add_book():
    title = request.form['title']
    link = request.form['link']

    all_books = Book.query.all()
    result = books_schema.dump(all_books)
    
    if (result): 
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
    print("\n\n\n\n\n\n" + all_books + "\n\n\n\n\n")
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

# endpoint to get the latest booklist
@app.route("/book2019/update", methods=["GET"])
def book_update_list():
    newBookList = get_books()

    all_books = Book.query.all()
    result = books_schema.dump(all_books)

    for book in newBookList: 
        title = ""
        link = ""

        for key, value in book.items(): 
            title = key
            link = value

        new_book = Book(title, link)
        db.session.add(new_book)
    
    db.session.commit()


    return "book list updated successfully"

if __name__ == '__main__':
    app.run(debug=True)