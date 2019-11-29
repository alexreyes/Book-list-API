from extensions import db
from models import Book

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