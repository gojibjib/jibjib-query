# [jibjib-query](https://github.com/gojibjib/jibjib-query)

This service utilizes [TensorFlow Serving](https://www.tensorflow.org/serving/) to load a [protobuffer-serialized](https://developers.google.com/protocol-buffers/) TensorFlow [model](https://github.com/gojibjib/jibjib-model) and make it accessible through a custom, [Flask-based](http://flask.pocoo.org/) REST API. 

>TensorFlow Serving is an open-source software library for serving machine learning models. It deals with the inference aspect of machine learning, taking models after training and managing their lifetimes, providing clients with versioned access via a high-performance, reference-counted lookup table.

## Repo layout
The complete list of JibJib repos is:

- [jibjib](https://github.com/gojibjib/jibjib): Our Android app. Records sounds and looks fantastic.
- [deploy](https://github.com/gojibjib/deploy): Instructions to deploy the JibJib stack.
- [jibjib-model](https://github.com/gojibjib/jibjib-model): Code for training the machine learning model for bird classification
- [jibjib-api](https://github.com/gojibjib/jibjib-api): Main API to receive database requests & audio files.
- [jibjib-data](https://github.com/gojibjib/jibjib-data): A MongoDB instance holding information about detectable birds.
- [jibjib-query](https://github.com/gojibjib/jibjib-query): A thin Python Flask API that handles communication with the [TensorFlow Serving](https://www.tensorflow.org/serving/) instance.
- [gopeana](https://github.com/gojibjib/gopeana): A API client for [Europeana](https://europeana.eu), written in Go.
- [voice-grabber](https://github.com/gojibjib/voice-grabber): A collection of scripts to construct the dataset required for model training

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