from app import db

class images(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.Text,nullable = False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)