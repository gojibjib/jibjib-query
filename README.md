# [jibjib-query](https://github.com/gojibjib/jibjib-query)

This service utilizes [TensorFlow Serving](https://www.tensorflow.org/serving/) to load a [protobuffer-serialized](https://developers.google.com/protocol-buffers/) TensorFlow [model](https://github.com/gojibjib/jibjib-model) and make it accessible through a custom, [Flask-based](http://flask.pocoo.org/) REST API.

## Installation
### Remotely
Use the [jibjib-api](https://github.com/gojibjib/jibjib-api) deployment [instructions](https://github.com/gojibjib/jibjib-query) to deploy the whole microservices stack to AWS.

### Locally
Clone the repo:

```
git clone https://github.com/gojibjib/jibjib-query
cd jibjib-query
```

Get the model:

```
wget https://s3-eu-west-1.amazonaws.com/jibjib/model/jibjib_model_serving.tgz
tar xzf jibjib_model_serving.tgz serve/
```

Get the mappings:

```
wget https://s3-eu-west-1.amazonaws.com/jibjib/pickle/mapping_pickles.tgz -O app/input/pickle
tar xzf app/input/pickle/mapping_pickes.tgz
rm app/input/pickle/*.tgz
```

Make sure to have [Docker](https://docs.docker.com/install/#server) and [Docker Compose](https://docs.docker.com/compose/install/) installed, then start the stack:

```
docker-compose up -d
```

Test it:

```
curl -H 'Content-Type: application/octet-stream' -X POST --data-binary @bird_voice.mp4 http://localhost:8081/detect/binary
```