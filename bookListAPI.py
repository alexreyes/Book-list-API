from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from extensions import db
from models import Book

from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname('sqlite:///books.sqlite'))
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

@app.route("/book2019/update", methods=["GET"])
def update_books():
    get_books()

    return "success"


def simple_get(url): 
    try: 
        with closing(get(url, stream=True)) as resp: 
            if is_good_response(resp): 
                return resp.content
            else: 
                return None

    except RequestException as e: 
        log_error("Error using requests to {0} : {1}".format(url, str(e)))

def is_good_response(resp): 
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)

def log_error(e):
    """
    It is always a good idea to log errors. 
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_books():
    url = 'https://www.goodreads.com/user_challenges/16171692'
    response = simple_get(url)
    
    soup = BeautifulSoup(response, 'html.parser')

    if response is not None: 
        
        for li in soup.find_all('li', attrs={'class': 'bookCoverContainer'}):
            title = li.find('img', alt=True)
            link = li.find('a', attrs={'class': 'bookCoverTarget'})
            
            if title['alt'] is not "":
                link = "https://www.goodreads.com" + link['href']
                new_book = Book(title['alt'], link)
                result = book_schema.dump(new_book)

                db.session.add(new_book)
                #file.write(title['alt'] + ' ,link: ' + "https://www.goodreads.com" + link['href'] + '\n')
    
    db.session.commit()
    #file.close()
    

if __name__ == '__main__':
    app.run(debug=True)