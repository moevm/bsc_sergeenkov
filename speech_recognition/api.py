from flask import (
    Flask,
    json,
    request
)

try:
    from .utils import *
except Exception as e:
    from utils import *

from wit import Wit


WIT_AI_ACCESS_TOKEN = 'JT3SXERNVLCVSECDCHN7NQE2H6EGMW6R'


app = Flask(__name__)
client = Wit(WIT_AI_KEY)


@app.route("/extract_text", methods=["POST"])
def extract_text_from_audio():
    """
    Извлечь текст из видеофайла
    """
    extracted_text = ""

    video_url = request.json['video_url']

    datetime_prefix = generate_filename_prefix()

    filename_prefix = 'data/' + datetime_prefix

    # Скачиваем видеофайл
    download_video(video_url=video_url, filename_prefix=filename_prefix)

    # Извлекаем аудиодорожку
    extract_sound_from_video(filename_prefix=filename_prefix)

    # Разделяем аудиодорожку
    split_audio(filename_prefix=filename_prefix)

    # Получаем список файлов
    audio_files = get_file_list_by_prefix(datetime_prefix + 'segment')

    # Извлекаем текст из аудиофайлов
    for audio_file in audio_files:
        extracted_text += ' ' + extract_text_from_audio(client=client, audio_filename='data/' + audio_file)

    response = app.response_class(
        response=json.dumps({
            "text": extracted_text
        }),
        status=200,
        mimetype='application/json'
    )
    return response
