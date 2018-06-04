import os
from flask import Flask
from flask_restful import Resource, Api

from resources.transformer import TransformMP3Form, TransformMP3Binary

UPLOAD_FOLDER = os.path.abspath('../uploads')
ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS

api = Api(app)
api.add_resource(TransformMP3Form, '/audio/transform/form')
api.add_resource(TransformMP3Binary, '/audio/transform/binary')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port= 8081, debug=True)