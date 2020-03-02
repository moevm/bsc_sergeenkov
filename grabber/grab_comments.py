import json

import requests

client_id = "G7FYKRNVUPlQKT8HmNvfbyysVUiRBnaFCSDcmBA9"
client_secret = "y9CCtrZ7jNyqWhsMF51Ca1lIfx8MtiZmEhK6akr3kEVU8AtYeL8orHaH5b9pOc3h9NcabM1bgMTgJTePshXMutDjjbfs5rTY07RLXyCfrOf7j0zaQrnoeWDeb491U5qx"
api_host = 'https://stepik.org'
course_id = 8057

auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
response = requests.post('https://stepik.org/oauth2/token/',
                         data={'grant_type': 'client_credentials'},
                         auth=auth)
token = response.json().get('access_token', None)
if not token:
    print('Unable to authorize with provided credentials')
    exit(1)


def fetch_object(obj_class, obj_id):
    api_url = '{}/api/{}s/{}'.format(api_host, obj_class, obj_id)
    response = requests.get(api_url,
                            headers={'Authorization': 'Bearer ' + token}).json()
    return response['{}s'.format(obj_class)][0]


def fetch_objects(obj_class, obj_ids, keep_order=True):
    objs = []
    # Fetch objects by 30 items,
    # so we won't bump into HTTP request length limits
    step_size = 30
    for i in range(0, len(obj_ids), step_size):
        obj_ids_slice = obj_ids[i:i + step_size]
        api_url = '{}/api/{}s?{}'.format(api_host, obj_class,
                                         '&'.join('ids[]={}'.format(obj_id)
                                                  for obj_id in obj_ids_slice))
        response = requests.get(api_url,
                                headers={'Authorization': 'Bearer ' + token}
                                ).json()

        objs += response['{}s'.format(obj_class)]
    if (keep_order):
        return sorted(objs, key=lambda x: obj_ids.index(x['id']))
    return objs


course = fetch_object('course', course_id)
sections = fetch_objects('section', course['sections'])

unit_ids = [unit for section in sections for unit in section['units']]
units = fetch_objects('unit', unit_ids)

lesson_ids = [unit['lesson'] for unit in units]
lessons = fetch_objects('lesson', lesson_ids)

step_ids = [step for lesson in lessons for step in lesson['steps']]
steps = fetch_objects('step', step_ids)

discussion_thread_ids = [discussion_thread for step in steps for discussion_thread in step['discussion_threads']]
discussion_threads = fetch_objects('discussion-thread', discussion_thread_ids)

discussion_proxy_ids = [discussion_thread['discussion_proxy'] for discussion_thread in discussion_threads]
discussion_proxies = fetch_objects('discussion-proxie', discussion_proxy_ids)

comment_ids = list(set([comment for discussion_proxy in discussion_proxies for comment in discussion_proxy['discussions']]))
comments = fetch_objects('comment', comment_ids, keep_order=False)

user_ids = list(set([comment['user'] for comment in comments]))
users = fetch_objects('user', comment_ids, keep_order=False)

print(len(comments))
print(len(users))

with open('data/comments.json', 'w') as file_obj:
    file_obj.write(json.dumps(comments, indent=2, ensure_ascii=False))

with open('data/users.json', 'w') as file_obj:
    file_obj.write(json.dumps(users, indent=2, ensure_ascii=False))
