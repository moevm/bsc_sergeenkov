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
            "_source": {"includes": ["title"]}
        }
    )

    answers = []

    print("{} total hits.".format(response["hits"]["total"]["value"]))
    for hit in response["hits"]["hits"]:
        answers.append(hit['_source'])
        print("id: {}, score: {}".format(hit["_id"], hit["_score"]))
        print(hit["_source"])
        print()

    return Response(answers, status=status.HTTP_200_OK)
