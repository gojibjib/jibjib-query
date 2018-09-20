import os
from flask import Flask
from flask_restful import Resource, Api

from resources.detect import DetectServing

SERVING_URL = os.environ.get("SERVING_URL", "localhost")
SERVING_PORT = os.environ.get("SERVING_PORT", 9000)
TRAIN_ID_LIST = os.environ.get("TRAIN_ID_LIST", "train_id_list.pickle")
BIRD_ID_MAP = os.environ.get("BIRD_ID_MAP", "bird_id_map.pickle")
MODEL_NAME = os.environ.get("MODEL_NAME", "jibjib_model")
UPLOAD_FOLDER = os.path.abspath('../uploads')
INPUT_FOLDER = os.path.abspath('../input')
MODEL_FOLDER = os.path.join(INPUT_FOLDER, 'model')
PICKLE_FOLDER = os.path.join(INPUT_FOLDER, 'pickle')

ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MODEL_FOLDER'] = MODEL_FOLDER
app.config['PICKLE_FOLDER'] = PICKLE_FOLDER
app.config['SERVING_URL'] = SERVING_URL
app.config['SERVING_PORT'] = int(SERVING_PORT)
app.config['MODEL_NAME'] = MODEL_NAME
app.config['TRAIN_ID_LIST'] = TRAIN_ID_LIST
app.config['BIRD_ID_MAP'] = BIRD_ID_MAP

api = Api(app)

api.add_resource(DetectServing, '/detect/binary')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 8081, debug=True)