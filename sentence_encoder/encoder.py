import json

import tensorflow_hub as hub
import tensorflow_text
import tensorflow as tf

from flask import Flask
from flask import request


app = Flask(__name__)

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")


@app.route("/encode-sentences", methods=["POST"])
def encode_text():
    data = request.json
    sentences = data["sentences"]
    vectors = embed(sentences)
    response = {'vectors': vectors.numpy().tolist()}
    return app.response_class(
        response=json.dumps(response),
        status=200,
        mimetype='application/json'
    )


if __name__ == "__main__":
    app.run()

