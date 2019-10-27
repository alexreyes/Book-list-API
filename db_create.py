from API import db
from models import Book

# create the database and the db tables
db.create_all()

# insert
db.session.add(Book("Good", "I\'m good"))
db.session.add(Book("Asdf", "I\'m asdf"))

# commit the changes
db.session.commit()
    