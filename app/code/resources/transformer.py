import os, uuid, hashlib
from flask import current_app, request
from flask_restful import Resource
from pydub import AudioSegment
from traceback import print_exc
from werkzeug.utils import secure_filename

from util.response import response
from util.system import rm_file

def allowed_filename(fname):
    return fname.split(".")[-1] in current_app.config["ALLOWED_EXTENSIONS"]

# Test with: #
# curl -v -X POST -F "file=@test.mp3" "http://localhost:8081/audio/transform/form"
class TransformMP3Form(Resource):
    """API resource to transform a .mp3 file into a .wav file"""

    def post(self):
        upload_folder = os.path.abspath(current_app.config["UPLOAD_FOLDER"])
        uploaded_file = request.files["file"]

        if not uploaded_file:
            return response(400, "No file uploaded", 0, None)

        if not allowed_filename(uploaded_file.filename):
            return response(400, "Invalid file", 0, None)

        # Convert audio
        wav_file = os.path.join(upload_folder, secure_filename(uploaded_file.filename.replace(".mp3", ".wav")))
        try:
            song = AudioSegment.from_mp3(uploaded_file)
        except:
            print_exc()
            return response(500, "Unable to load file", 0, None)

        try:
            song.export(wav_file, format="wav")
        except:
            print_exc()
            return response(500, "Unable to transform file to wav", 0, None)

        #return response(202, "File saved to {}".format(wav_file), 0, None)
        # For testing, remove file again
        rm_file(wav_file)
        return response(202, "File OK", 0, None)

class TransformMP3Binary(Resource):
    """API Resource to accept a binary file via stream and transform it into .wav"""

    # Test with:
    # curl -v -H 'Content-Type: application/octet-stream' -X POST --data-binary @test.mp3 https://localhost:8081/audio/transform/binary
    def post(self):
        upload_folder = os.path.abspath(current_app.config["UPLOAD_FOLDER"])
        file_name = str(uuid.uuid4())
        file_path = os.path.join(upload_folder, file_name)

        # Accept binary file file
        try:
            with open(file_path, "wb") as wf:
                chunk_size = 4096
                while True:
                    chunk = request.stream.read(chunk_size)
                    if len(chunk) == 0:
                        break

                    wf.write(chunk)
        except:
            print_exc()
            rm_file(wav_file)
            return response(500, "Internal error occured while trying to upload file", 0, None)

        if not os.path.isfile(file_path) or os.path.getsize(file_path) <= 0:
            print("File {} doesn't exist".format(file_path))
            return response(400, "Uploaded file hasn't been saved", 0, None)
        else:
            print("File saved to {}, size: {}".format(file_path, os.path.getsize(file_path)))
        

        # Transform file into wav
        try:
            song = AudioSegment.from_mp3(file_path)
        except:
            print_exc()
            rm_file(file_path)
            return response(500, "Unable to load mp3 file", 0, None)
        wav_file = os.path.join(upload_folder, file_name + ".wav")
        try:
            song.export(wav_file, format="wav")
        except:
            print_exc()
            rm_file(file_path)
            return response(500, "Unable to transform file to wav", 0, None)

        rm_file(file_path)
        # return response(202, "File saved to {}".format(file_path), 0, None)
        
        # For testing, remove file again
        rm_file(wav_file)
        return response(202, "File OK", 0, None)