import asyncio

from datetime import datetime

import subprocess

import os

import requests

from wit import Wit

WIT_AI_ACCESS_TOKEN = 'JT3SXERNVLCVSECDCHN7NQE2H6EGMW6R'


def generate_filename_prefix() -> str:
    """
    Сгенерировать уникальный префикс для имен временных файлов и директорий
    :return: str - текстовая строка, представляющая префикс на основе даты и времени
    """
    return datetime.now().strftime('%m-%d-%Y_%H:%M:%S_')


def download_video(video_url, filename_prefix) -> None:
    """
    Сохранить видеофайл по указанной ссылке
    :param video_url: URL, по которому расположен видеоролик
    :param filename_prefix: префикс названия файла для сохранения
    """
    response = requests.get(video_url)
    with open("{0}.mp4".format(filename_prefix), "wb") as handle:
        for data in response.iter_content():
            handle.write(data)


def extract_sound_from_video(filename_prefix) -> None:
    """
    Извлечь из видеофайла аудиодорожку
    :param filename_prefix: префикс названия файла для сохранения
    """
    command = "ffmpeg -i {0}.mp4 -ab 160k -ac 2 -ar 44100 -vn {0}.wav".format(
        filename_prefix
    )
    subprocess.call(command, shell=True)


def split_audio(filename_prefix, segment_length=15) -> None:
    """
    Разделить длинный аудиофайл на короткие сегменты
    :param filename_prefix: префикс названия файла для сохранения
    :param segment_length: длина сегмента
    """
    command = "ffmpeg -i {0}.wav -f segment -segment_time {1} -c copy {0}segment_%03d.wav".format(
        filename_prefix, segment_length
    )
    subprocess.call(command, shell=True)


def get_file_list_by_prefix(filename_prefix, path='data') -> list:
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
    file_list.sort()
    return file_list


async def extract_text_from_audio_file(wit_client, audio_filename) -> str:
    """
    Получить текст из аудио-файла

    :param wit_client: объект класса Wit для работы с API wit.ai
    :param audio_filename: путь к аудио-файлу
    :return: str - текстовая строка с распознанной речью
    """
    with open(audio_filename, 'rb') as audio:
        response = wit_client.speech(audio, None, {'Content-Type': 'audio/wav'})
        print(response)
    return response['text']


def clear_data_directory(path='data'):
    """
    Очистить директорию с временными файлами

    :param path: str - путь к директории с временными файлами
    :return:
    """
    os.system('rm -rf {0}/*'.format(path))


async def video_to_text(video_url) -> str:
    """
    Извлечь текст из видеофайла

    Функция использует описанные выше функции

    :param video_url: URL видео файла
    :param wit_api_key: Ключ API wit.ai
    :return: str - текстовая строка с распознанной речью
    """
    extracted_text = ""

    video_url = video_url

    datetime_prefix = generate_filename_prefix()

    filename_prefix = 'data/' + datetime_prefix

    try:
        # Скачиваем видеофайл
        download_video(video_url=video_url, filename_prefix=filename_prefix)

        # Извлекаем аудиодорожку
        extract_sound_from_video(filename_prefix=filename_prefix)

        # Разделяем аудиодорожку
        split_audio(filename_prefix=filename_prefix)

        # Получаем список файлов
        audio_files = get_file_list_by_prefix(datetime_prefix + 'segment')

        print(audio_files)

        wit_client = Wit(WIT_AI_ACCESS_TOKEN)

        tasks = [asyncio.create_task(extract_text_from_audio_file(wit_client=wit_client, audio_filename='data/' + filename)) for filename in
                 audio_files]

        extracted_chunks = await asyncio.gather(*tasks)
        for chunk in extracted_chunks:
            extracted_text += chunk + ' '

        # # Извлекаем текст из аудиофайлов
        # for audio_file in audio_files:
        #     print(audio_file)
        #     text = extract_text_from_audio_file(wit_client=wit_client, audio_filename='data/' + audio_file)
        #     extracted_text += ' '
        #     extracted_text += text
    finally:
        clear_data_directory()

    return extracted_text.strip()


if __name__ == '__main__':
    text = asyncio.run(video_to_text('https://ucarecdn.com/922fa667-de21-44b6-8a47-8f1014f8ee3f/24298_360_bc64347f86cd95b2f8a769d02914afb0.mp4'))
    with open('test.txt', 'w') as text_file:
        text_file.write(text)
