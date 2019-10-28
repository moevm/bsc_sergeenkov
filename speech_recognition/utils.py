from datetime import datetime

import subprocess

import os

import requests


def generate_filename_prefix():
    """
    Сгенерировать уникальный префикс для имен временных файлов и директорий
    :return: str - текстовая строка, представляющая префикс на основе даты и времени
    """
    return datetime.now().strftime('%m-%d-%Y_%H:%M:%S_')


def download_video(video_url, filename_prefix):
    """
    Сохранить видеофайл по указанной ссылке
    :param video_url: URL, по которому расположен видеоролик
    :param filename_prefix: префикс названия файла для сохранения
    """
    response = requests.get(video_url)
    with open("{0}.mp4".format(filename_prefix), "wb") as handle:
        for data in response.iter_content():
            handle.write(data)


def extract_sound_from_video(filename_prefix):
    """
    Извлечь из видеофайла аудиодорожку
    :param filename_prefix: префикс названия файла для сохранения
    """
    command = "ffmpeg -i {0}.mp4 -ab 160k -ac 2 -ar 44100 -vn {0}.wav".format(
        filename_prefix
    )
    subprocess.call(command, shell=True)


def split_audio(filename_prefix, segment_length=15):
    """
    Разделить длинный аудиофайл на короткие сегменты
    :param filename_prefix: префикс названия файла для сохранения
    :param segment_length: длина сегмента
    """
    command = "ffmpeg -i {0} -f segment -segment_time {1} -c copy {0}segment_%03d.wav".format(
        filename_prefix, segment_length
    )
    subprocess.call(command, shell=True)


def get_file_list_by_prefix(filename_prefix, path='data'):
    """
    Получить список файлов, начинающихся с заданного префикса

    :param filename_prefix: префикс для поиска файлов
    :param path: директория
    :return:
    """
    file_list = list()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.startswith(filename_prefix):
                file_list.append(file)


def get_text_from_audio_file(wit_client, audio_filename):
    """
    Получить текст из аудио-файла

    :param wit_client: объект класса Wit для работы с API wit.ai
    :param audio_filename: путь к аудио-файлу
    :return: str - текстовая строка с распознанной речью
    """
    with open(audio_filename, 'rb') as audio:
        response = wit_client.post_speech(data=audio)
    return response['_text']
