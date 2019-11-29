from extensions import db 


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    link = db.Column(db.String(120), unique=True)

    def __init__(self, title, link):
        self.title = title
        self.link = link

