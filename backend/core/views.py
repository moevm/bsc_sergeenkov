from rest_framework.decorators import (
    api_view,
    permission_classes
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.conf import settings

import requests

from elasticsearch import Elasticsearch


def get_sentence_vector(sentence):
    response = requests.post(
        url=settings.ENCODER_URL,
        json={'sentences': [sentence]}
    )
    if response.status_code != 200:
        raise Exception('Encoder error')
    return response.json()['vectors'][0]


@api_view(['POST'])
@permission_classes([AllowAny, ])
def search_similar_questions(request):
    client = Elasticsearch(settings.ELASTICSEARCH_URL)
    query_vector = get_sentence_vector(request.data['question'])
    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['title_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    response = client.search(
        index=settings.INDEX_NAME,
        body={
            "size": 5,
            "query": script_query,
            "_source": {"includes": ["title", "_id", "django_id"]}
        }
    )

    answers = []

    index = 0

    print("{} total hits.".format(response["hits"]["total"]["value"]))
    for hit in response["hits"]["hits"]:
        el = hit['_source']
        el['id'] = index
        index += 1
        answer = hit['_source']
        answer.update({
            'score': round(hit["_score"], 1),
            'user': {
                'fullname': 'Иван Иванов',
                'avatar': 'https://sun6-13.userapi.com/GzeOxk5ZZywlZlNOXvF7NCUd7tG69Pv6dXLg8w/U1lYMf98a_c.jpg?ava=1'
            },
            'answer': 'Текст ответа блаблаблаблабла'
        })
        answers.append(answer)
        print("id: {}, score: {}".format(hit["_id"], hit["_score"]))
        print(hit["_source"])
        print()

    return Response(answers, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def search_course_materials(request):
    client = Elasticsearch(settings.ELASTICSEARCH_URL)
    query_vector = get_sentence_vector(request.data['question'])

    script_query = {
        "script_score": {
            "query": {"match_all": {}},
            "script": {
                "source": "cosineSimilarity(params.query_vector, doc['content_vector']) + 1.0",
                "params": {"query_vector": query_vector}
            }
        }
    }

    response = client.search(
        index=settings.COURSE_MATERIALS_INDEX_NAME,
        body={
            "size": 5,
            "query": script_query,
            "_source": {"includes": [
                "content",
                "_id",
                "django_id",
                "course_id",
                "lesson_name",
                "lesson_id",
                "step_id",
                "url"
            ]}
        }
    )

    answers = []

    index = 0

    print("{} total hits.".format(response["hits"]["total"]["value"]))
    for hit in response["hits"]["hits"]:
        el = hit['_source']
        el['id'] = index
        index += 1
        answer = hit['_source']
        answer.update({'score': round(hit["_score"], 1)})
        answers.append(answer)
        print("id: {}, score: {}".format(hit["_id"], hit["_score"]))
        print(hit["_source"])
        print()

    return Response(answers, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def mark_material_as_answer(request):
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def ask_question_manual(request):
    return Response(status=status.HTTP_200_OK)
