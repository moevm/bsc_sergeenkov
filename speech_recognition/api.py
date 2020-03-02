from flask import (
    Flask,
    json,
    request
)

try:
    from .utils import video_to_text
except Exception as e:
    from utils import video_to_text

app = Flask(__name__)


@app.route("/extract_text", methods=["POST"])
def extract_text_from_audio():
    """
    Извлечь текст из видеофайла
    """
    text = video_to_text(video_url=request.json['video_url'])
    response = app.response_class(
        response=json.dumps({
            "text": text
        }),
        status=200,
        mimetype='application/json'
    )
    return response
