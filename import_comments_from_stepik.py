import os

import requests

from pymongo import MongoClient

MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_PORT = int(os.environ.get('MONGO_PORT', '27017'))
MONGO_DB_NAME = 'stepik_comments'
MONGO_COLLECTION_NAME = 'Comment'

STEPIK_API_URL = 'https://stepik.org/api/comments'
STEPIK_COURSE_ID = 10524


def import_comments():
    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]

    has_next_page = True
    page_number = 1

    while has_next_page:
        print('Downloading page {page_number}'.format(page_number=page_number))

        response = requests.get(
            url=STEPIK_API_URL,
            params={
                'course': STEPIK_COURSE_ID,
                'page': page_number
            }
        ).json()

        print(len(response['comments']))

        page_number = response['meta']['page'] + 1
        has_next_page= response['meta']['has_next']

        if len(response['comments']):
            collection.insert_many(response['comments'])


if __name__ == '__main__':
    import_comments()
