import os, pickle, uuid, time
from flask_restful import Resource
from flask import current_app as app
from flask import request
from traceback import print_exc

# TensorFlow serving stuff to send messages
from grpc.beta import implementations
from tensorflow_serving.apis import predict_pb2
from tensorflow_serving.apis import prediction_service_pb2
from tensorflow.contrib.util import make_tensor_proto

# VGGish stuff
import numpy as np
import tensorflow as tf
from util import vggish_input
from util import vggish_params
from util import vggish_slim

# API stuff
from util.system import rm_file, mp3_to_wav, mp4_to_wav
from util.response import response

class DetectServing(Resource):
    def post(self):
        upload_folder = os.path.abspath(app.config["UPLOAD_FOLDER"])
        file_name = str(uuid.uuid4())
        mp3_path = os.path.join(upload_folder, file_name)
        train_id_list_path = os.path.join(app.config["PICKLE_FOLDER"], app.config["TRAIN_ID_LIST"])
        bird_id_map_path = os.path.join(app.config["PICKLE_FOLDER"], app.config["BIRD_ID_MAP"])

        # Load pickle files
        pickle.HIGHEST_PROTOCOL
        train_id_list = None
        try:
            with open(train_id_list_path, "rb") as rf:
                train_id_list = pickle.load(rf)
        except:
            print_exc()
            return response(500, "An internal error occured", 0, None)
        # print(train_id_list)

        bird_id_map = None
        try:
            with open(bird_id_map_path, "rb") as rf:
                bird_id_map = pickle.load(rf)
        except:
            print_exc()
            return response(500, "An internal error occured", 0, None)
        # print(bird_id_map)

        # Accept binary file file
        try:
            with open(mp3_path, "wb") as wf:
                chunk_size = 4096
                while True:
                    chunk = request.stream.read(chunk_size)
                    if len(chunk) == 0:
                        break

                    wf.write(chunk)
        except:
            print_exc()
            rm_file(mp3_path)
            return response(500, "An error occured while trying to upload file", 0, None)
        
        # Check if it has been saved
        if not os.path.isfile(mp3_path) or os.path.getsize(mp3_path) <= 0:
            print("File {} doesn't exist".format(mp3_path))
            return response(500, "Uploaded file could not been saved", 0, None)
        else:
            # print("File saved to {}, size: {}".format(mp3_path, os.path.getsize(mp3_path)))
            pass

        # Transform to WAV
        # TODO: use query stringd to accept different audio formats
        wav_path = mp4_to_wav(mp3_path, file_name + ".wav")
        if wav_path is None:
            rm_file(mp3_path)
            return response(500, "An error occured while trying to convert file to WAV", 0, None)

        try:
            my_input = vggish_input.wavfile_to_examples(wav_path)
        except:
            print_exc()
            rm_file(mp3_path)
            rm_file(wav_path)   
            return response(400, "Unable to extract spectogram, file seems to be corrupted", 0, None)

        # Query TF Serving instance
        try:
            host = app.config["SERVING_URL"]
            port = app.config["SERVING_PORT"]
            channel = implementations.insecure_channel(host, port)
            stub = prediction_service_pb2.beta_create_PredictionService_stub(channel)

            start = time.time()
            req = predict_pb2.PredictRequest()
            req.model_spec.name = app.config["MODEL_NAME"]
            req.model_spec.signature_name = tf.saved_model.signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY
            req.inputs['inputs'].CopyFrom(make_tensor_proto(my_input, dtype=tf.float32))
            result = stub.Predict(req, 30.0)
            end = time.time()
            # print("Finished query after {}s".format(end - start))

            pred = [x for x in result.outputs["outputs"].float_val]
            size_vector = int(result.outputs["outputs"].tensor_shape.dim[0].size)
            num_classes = int(result.outputs["outputs"].tensor_shape.dim[1].size)
            # print("len(pred): {}, size_vector: {}, num_classes: {}".format(len(pred), size_vector, num_classes))

        except:
            print_exc()
            rm_file(mp3_path)
            rm_file(wav_path)   
            return response(500, "An error occured while trying to query Serving instance", 0, None)

        # Tuning
        try:
            out_array = np.zeros(num_classes)
            for i in range(0, len(pred), num_classes):
                for j in range(num_classes):
                    out_array[j] += pred[i+j] * pred[i+j]

            out_list = out_array.tolist()
            sorted_array = sorted(out_list)

            # 1st, 2nd, 3rd accumulated values
            first, second, third = sorted_array[-1], sorted_array[-2], sorted_array[-3]

            # 1st, 2nd, 3rd Train IDs
            first_bird, second_bird, third_bird = out_list.index(first), out_list.index(second), out_list.index(third)

            # Getting confidences
            sum_acc = sum([first, second, third])
            first_conf, second_conf, third_conf = first / sum_acc, second / sum_acc, third / sum_acc

            # print(first, second, third)
            # print(first_bird, second_bird, third_bird)
            # print(first_conf, second_conf, third_conf)
        except:
            print_exc()
            rm_file(mp3_path)
            rm_file(wav_path)
            return response(500, "An error occured while trying to calculate accuracies", 0, None)

        out = []
        try:
            out = [
                {"id": bird_id_map[train_id_list[int(first_bird)]],
                "accuracy": first_conf},
                {"id": bird_id_map[train_id_list[int(second_bird)]],
                "accuracy": second_conf},
                {"id": bird_id_map[train_id_list[int(third_bird)]],
                "accuracy": third_conf}
            ]
        except KeyError:
            print_exc()
            rm_file(mp3_path)
            rm_file(wav_path)
            return response(400, "No clear bird could be identified", 0, None)

        except Exception:
            print_exc()
            rm_file(mp3_path)
            rm_file(wav_path)
            return response(500, "An error occured while trying to construct response", 0, None)

        rm_file(mp3_path)
        rm_file(wav_path)
        return response(200, "Detection successful", len(out), out)