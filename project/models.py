from project import db

class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def __init__(self, title, description): 
        self.title = title
        self.description = description

    def __repr__(self): 
        return '<title {}'.format(self.title)
