from .app import db

class images(db.Model):
    
    __tablename__ = "images"
    
    id = db.Column(db.Integer, primary_key = True)
    image = db.Column(db.Text,nullable = False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text)
    
    def __init__(self,image, name, mimetype, description):
        self.image = image
        self.name = name 
        self.mimetype = mimetype 
        self.description = description 