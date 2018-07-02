# [jibjib-query](https://github.com/gojibjib/jibjib-query)

This service utilizes [TensorFlow Serving](https://www.tensorflow.org/serving/) to load a [protobuffer-serialized](https://developers.google.com/protocol-buffers/) TensorFlow [model](https://github.com/gojibjib/jibjib-model) and make it accessible through a custom, [Flask-based](http://flask.pocoo.org/) REST API. 

>TensorFlow Serving is an open-source software library for serving machine learning models. It deals with the inference aspect of machine learning, taking models after training and managing their lifetimes, providing clients with versioned access via a high-performance, reference-counted lookup table.

## Installation
### Remotely
Use the [jibjib-api](https://github.com/gojibjib/jibjib-api) deployment [instructions](https://github.com/gojibjib/jibjib-api/tree/master/deploy) to deploy the whole microservices stack to AWS.

### Locally
Clone the repo:

```
git clone https://github.com/gojibjib/jibjib-query
cd jibjib-query
```

Get the model:

```
curl https://s3-eu-west-1.amazonaws.com/jibjib/model/jibjib_model_serving.tgz | tar -xvz -C app/input/model/
```

Get the mappings:

```
curl https://s3-eu-west-1.amazonaws.com/jibjib/pickle/mapping_pickles.tgz | tar -xvz -C app/input/pickle
```

Make sure to have [Docker](https://docs.docker.com/install/#server) and [Docker Compose](https://docs.docker.com/compose/install/) installed, then start the stack:

```
docker-compose up -d
```

Test it:

```
curl -H 'Content-Type: application/octet-stream' -X POST --data-binary @bird_voice.mp4 http://localhost:8081/detect/binary
```