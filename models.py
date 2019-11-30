from extensions import db 

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=False)
    link = db.Column(db.String(120), unique=False)

    def __init__(self, title, link):
        self.title = title
        self.link = link

