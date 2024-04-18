from flask import Flask,jsonify,request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from gpt_manager import generate_image_description
import base64
import os



app = Flask(__name__)
    
CORS(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://hozandagbxumsc:32f4337aff757b3a200d33b00b307cf4348fd45a2249a65a46de6dc169b2c784@ec2-54-156-185-205.compute-1.amazonaws.com:5432/da63fboq5n8adi'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy()


db.init_app(app)
with app.app_context():
    db.create_all()


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
    
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/')
def home():
    return "Hello world"

@app.route('/upload', methods = ['POST'])
def upload():

    pic = request.files['pic']
    if not pic:
        return jsonify({"error": "No file found"}), 400
    filename = pic.filename
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return jsonify({"error": "Bad upload"}), 400

    image_content = pic.read()
    description = generate_image_description(image_content)
    
    img = images(image=image_content, name=filename, mimetype=mimetype, description= description)
    db.session.add(img)
    db.session.commit()
    
    return jsonify({"message": "Image Uploaded", "description": description}), 200

@app.route('/images', methods=['GET'])
def get_images():
    all_images = images.query.all()
    image_list = []
    for image in all_images:
        image_data = {
            'id': image.id,
            'image': base64.b64encode(image.image).decode('utf-8'),  # Convert bytes to base64 string
            'name': image.name,
            'mimetype': image.mimetype,
            'description': image.description
        }
        image_list.append(image_data)
    return jsonify(image_list)


if __name__ == "__main__":
    app.run(debug=True)