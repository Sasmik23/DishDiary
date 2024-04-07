from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import images
from db import db_init, db
from gpt_manager import generate_image_description
import base64


app = Flask(__name__)
    
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xxsbhhpozcgvyy:e25d18ebd43c02b777cf0413a15aa6f3b38abee6879f0e6801dd8f039c287fc5@ec2-34-193-110-25.compute-1.amazonaws.com:5432/dtpj3qnei78r'
app.config['SQLAlCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
db_init(app)


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