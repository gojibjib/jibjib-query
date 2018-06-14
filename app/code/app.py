import os
from flask import Flask
from flask_restful import Resource, Api

from resources.detect import DetectBinary, DetectServing

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

api = Api(app)

# with app.app_context():
#     g.tf_session = get_tf_session()

# api.add_resource(TransformMP3Form, '/audio/transform/multipart')
# api.add_resource(TransformMP3Binary, '/audio/transform/binary')
api.add_resource(DetectBinary, '/detect/binary')
api.add_resource(DetectServing, '/detect/serving')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port= 8081, debug=True)