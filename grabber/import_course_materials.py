import asyncio

import sys

import json

import os

import requests

from pymongo import MongoClient

from utils import get_token, remove_html_tags, clear_string

sys.path.append('/home/mikhail/PycharmProjects/bsc_sergeenkov')

from speech_recognition.utils import video_to_text

COURSE_ID = '14736'
CLIENT_ID = 'G7FYKRNVUPlQKT8HmNvfbyysVUiRBnaFCSDcmBA9'
CLIENT_SECRET = 'y9CCtrZ7jNyqWhsMF51Ca1lIfx8MtiZmEhK6akr3kEVU8AtYeL8orHaH5b9pOc3h9NcabM1bgMTgJTePshXMutDjjbfs5rTY07RLXyCfrOf7j0zaQrnoeWDeb491U5qx'

MONGO_HOST = os.environ.get('MONGO_HOST', '100.124.0.7')
MONGO_PORT = int(os.environ.get('MONGO_PORT', '32247'))
MONGO_DB_NAME = 'stepik_course_data'
MONGO_COLLECTION_NAME = 'stepik_course_materials'


async def extract_step_coroutine(step_id, lesson, unit, token):
    step_page = requests.get(
        url='https://stepik.org/api/steps/{}'.format(step_id),
        headers={'Authorization': 'Bearer ' + token}
    ).json()
    step = step_page['steps'][0]
    content = None
    if step['block']['name'] == 'text':
        content = clear_string(remove_html_tags(step['block']['text']))
    elif step['block']['name'] == 'video':
        content = await video_to_text(step['block']['video']['urls'][-1]['url'])
    result = {
        'lesson_name': lesson['title'],
        'type': step['block']['name'],
        'step_id': step['id'],
        'lesson_id': lesson['id'],
        'content': content,
        'rating': 1,
        'url': 'https://stepik.org/lesson/{0}/step/{1}?unit={2}'.format(
            lesson['id'],
            step['position'],
            unit['id']
        )
    }
    return result


async def extract_unit_coroutine(unit_id, token):
    unit_page = requests.get(
        url='https://stepik.org/api/units/{}'.format(unit_id),
        headers={'Authorization': 'Bearer ' + token}
    ).json()
    unit = unit_page['units'][0]
    lesson_page = requests.get(
        url='https://stepik.org/api/lessons/{}'.format(unit['lesson']),
        headers={'Authorization': 'Bearer ' + token}
    ).json()
    lesson = lesson_page['lessons'][0]

    print('\t Импорт урока \"{}\"'.format(lesson['title']))

    tasks = [asyncio.create_task(extract_step_coroutine(step_id, lesson, unit, token)) for step_id in lesson['steps']]
    extracted_steps = await asyncio.gather(*tasks)
    return extracted_steps


async def extract_section_coroutine(section_id, token):
    section_page = requests.get(
        url='https://stepik.org/api/sections/{}'.format(section_id),
        headers={'Authorization': 'Bearer ' + token}
    ).json()
    section = section_page['sections'][0]
    print('Импорт раздела \"{}\"'.format(section['title']))
    tasks = [asyncio.create_task(extract_unit_coroutine(unit_id, token)) for unit_id in section['units']]
    extracted_steps = await asyncio.gather(*tasks)
    return extracted_steps


async def import_course_materials(course_id):
    # client = MongoClient(MONGO_HOST, MONGO_PORT)
    # db = client[MONGO_DB_NAME]
    # collection = db[MONGO_COLLECTION_NAME]
    # collection.drop()

    token = get_token(CLIENT_ID, CLIENT_SECRET)

    course_page = requests.get(
        url='https://stepik.org/api/courses/{}'.format(course_id),
        headers={'Authorization': 'Bearer ' + token}
    ).json()
    course = course_page['courses'][0]
    print(course['title'])
    print()

    tasks = [asyncio.create_task(extract_section_coroutine(section_id, token)) for section_id in course['sections']]
    #
    for section_id in course['sections']:
        section_page = requests.get(
            url='https://stepik.org/api/sections/{}'.format(section_id),
            headers={'Authorization': 'Bearer ' + token}
        ).json()
        section = section_page['sections'][0]
    #     print('Импорт раздела \"{}\"'.format(section['title']))
    #
    #     for unit_id in section['units']:
    #         unit_page = requests.get(
    #             url='https://stepik.org/api/units/{}'.format(unit_id),
    #             headers={'Authorization': 'Bearer ' + token}
    #         ).json()
    #         unit = unit_page['units'][0]
    #         lesson_page = requests.get(
    #             url='https://stepik.org/api/lessons/{}'.format(unit['lesson']),
    #             headers={'Authorization': 'Bearer ' + token}
    #         ).json()
    #         lesson = lesson_page['lessons'][0]
    #
    #         print('\t Импорт урока \"{}\"'.format(lesson['title']))
    #
    #         for step_id in lesson['steps']:
    #             step_page = requests.get(
    #                 url='https://stepik.org/api/steps/{}'.format(step_id),
    #                 headers={'Authorization': 'Bearer ' + token}
    #             ).json()
    #             step = step_page['steps'][0]
    #             if step['block']['name'] == 'text':
    #                 content = clear_string(remove_html_tags(step['block']['text']))
    #
    #                 collection.insert_one({
    #                     'type': 'text',
    #                     'lesson_name': lesson['title'],
    #                     'step_id': step['id'],
    #                     'lesson_id': lesson['id'],
    #                     'content': content,
    #                     'rating': 0,
    #                     'url': 'https://stepik.org/lesson/{0}/step/{1}?unit={2}'.format(
    #                         lesson['id'],
    #                         step['position'],
    #                         unit['id']
    #                     )
    #                 })
    #
    #             elif step['block']['name'] == 'video':
    #                 content = video_to_text(step['block']['video']['urls'][-1]['url'])
    #                 collection.insert_one({
    #                     'type': 'video',
    #                     'lesson_name': lesson['title'],
    #                     'step_id': step['id'],
    #                     'lesson_id': lesson['id'],
    #                     'content': content,
    #                     'rating': 1,
    #                     'url': 'https://stepik.org/lesson/{0}/step/{1}?unit={2}'.format(
    #                         lesson['id'],
    #                         step['position'],
    #                         unit['id']
    #                     )
    #                 })
    extracted_steps = await asyncio.gather(*tasks)
    with open('course_dump', 'w') as text_file:
        text_file.write(json.dumps(extracted_steps, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    asyncio.run(import_course_materials(COURSE_ID))
