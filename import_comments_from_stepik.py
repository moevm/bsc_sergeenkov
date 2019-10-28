import os

import csv

import requests

from pymongo import MongoClient

MONGO_HOST = os.environ.get('MONGO_HOST', '100.124.0.7')
MONGO_PORT = int(os.environ.get('MONGO_PORT', '32247'))
MONGO_DB_NAME = 'stepik_comments'
MONGO_COLLECTION_NAME = 'comments_raw'

STEPIK_API_URL = 'https://stepik.org/api/comments'
STEPIK_COURSE_ID = '10524'
STEPIK_USER_ID = '19677749'

CLIENT_ID = 'G7FYKRNVUPlQKT8HmNvfbyysVUiRBnaFCSDcmBA9'
CLIENT_SECRET = 'y9CCtrZ7jNyqWhsMF51Ca1lIfx8MtiZmEhK6akr3kEVU8AtYeL8orHaH5b9pOc3h9NcabM1bgMTgJTePshXMutDjjbfs5rTY07RLXyCfrOf7j0zaQrnoeWDeb491U5qx'

fields = ['id', 'parent', 'user',
          'user_role', 'time', 'last_time',
          'text', 'reply_count', 'is_deleted',
          'deleted_by', 'deleted_at', 'can_edit',
          'can_moderate', 'can_delete', 'actions',
          'target', 'replies', 'subscriptions',
          'is_pinned', 'pinned_by', 'pinned_at',
          'is_staff_replied', 'is_reported', 'attachments',
          'thread', 'submission', 'edited_by',
          'edited_at', 'epic_count', 'abuse_count',
          'vote', 'translations']


def get_token(client_id, client_secret):
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post('https://stepik.org/oauth2/token/',
                             data={'grant_type': 'client_credentials'},
                             auth=auth)
    token = response.json().get('access_token', None)
    if not token:
        print('Unable to authorize with provided credentials')
        exit(1)
    return token


def get_course(token, course_id):
    api_url = 'https://stepik.org/api/courses/{}'.format(course_id)
    response = requests.get(url=api_url,
                            headers={'Authorization': 'Bearer ' + token})
    course_page = response.json()
    return course_page


def get_lessons_page(token, course_id, page_id):
    api_url = 'https://stepik.org/api/lessons'
    response = requests.get(
        url=api_url,
        params={
            'course': course_id,
            'page': page_id
        },
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    lessons_page = response.json()
    return lessons_page


def get_lessons(token, course_id):
    page = 1
    lessons_page = get_lessons_page(token, course_id, page)
    lessons = []
    while lessons_page['meta']['has_next']:
        lessons += lessons_page['lessons']
        page += 1
        lessons_page = get_lessons_page(token, course_id, page)

    return lessons


def get_comments_page(token, course_id, step_id, page_id):
    api_url = 'https://stepik.org/api/comments'
    response = requests.get(
        url=api_url,
        params={
            'course': course_id,
            # 'target': step_id,
            'page': page_id
        },
        headers={
            'Authorization': 'Bearer ' + token
        }
    )
    comments_page = response.json()
    return comments_page


def import_comments():
    token = get_token(CLIENT_ID, CLIENT_SECRET)

    csv_output_file = csv.writer(open("comments_raw.csv", "w", encoding='utf-8'), dialect='excel-tab')
    csv_output_file.writerow(fields)

    client = MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[MONGO_DB_NAME]
    collection = db[MONGO_COLLECTION_NAME]
    collection.drop()

    comments_count = 0

    page = 0
    has_next_page = True
    while has_next_page:
        page += 1
        comments_page = get_comments_page(token, STEPIK_COURSE_ID, None, page)
        for comment in comments_page['comments']:
            comments_count += 1
            print(comment['text'])
            csv_output_file.writerow([str(comment[field]) for field in fields])

            collection.insert_one(comment)

        has_next_page = comments_page['meta']['has_next']

    print('Импортировано комментариев: {}'.format(comments_count))


if __name__ == '__main__':
    import_comments()
