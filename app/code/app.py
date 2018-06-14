import os
from flask import Flask
from flask_restful import Resource, Api

from resources.detect import DetectBinary, DetectServing

SERVING_URL = os.environ.get("SERVING_URL", "localhost")
SERVING_PORT = os.environ.get("SERVING_PORT", 9000)
MODEL_NAME = os.environ.get("MODEL_NAME", "jibjib_model")
UPLOAD_FOLDER = os.path.abspath('../uploads')
INPUT_FOLDER = os.path.abspath('../input')
MODEL_FOLDER = os.path.join(INPUT_FOLDER, 'model')
MODEL = os.path.join(MODEL_FOLDER, "jibjib_model.ckpt")
PICKLE_FOLDER = os.path.join(INPUT_FOLDER, 'pickle')

ALLOWED_EXTENSIONS = set(['mp3'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS
app.config['MODEL_FOLDER'] = MODEL_FOLDER
app.config['MODEL'] = MODEL
app.config['PICKLE_FOLDER'] = PICKLE_FOLDER
app.config['SERVING_URL'] = SERVING_URL
app.config['SERVING_PORT'] = int(SERVING_PORT)
app.config['MODEL_NAME'] = MODEL_NAME

api = Api(app)

api.add_resource(DetectServing, '/detect/binary')
# api.add_resource(DetectServing, '/detect/serving')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 8081, debug=True)