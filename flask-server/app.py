from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import images
from gpt_manager import generate_image_description
import base64



app = Flask(__name__)
    
CORS(app)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hozandagbxumsc:32f4337aff757b3a200d33b00b307cf4348fd45a2249a65a46de6dc169b2c784@ec2-54-156-185-205.compute-1.amazonaws.com:5432/da63fboq5n8adi'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
db = SQLAlchemy()

db.init_app(app)
with app.app_context():
    db.create_all()


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