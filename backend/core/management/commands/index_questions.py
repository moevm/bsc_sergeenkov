import requests

from django.core.management.base import BaseCommand

from django.conf import settings

from core.models import Question

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class Command(BaseCommand):
    help = 'Скрипт для индексирования вопросв в ES'

    def handle(self, *args, **kwargs):
        questions = Question.objects.all()
        question_texts = [question.question for question in questions]

        client = Elasticsearch(settings.ELASTICSEARCH_URL)
        client.indices.delete(index=settings.INDEX_NAME, ignore=[404])
        with open(settings.INDEX_FILE) as index_file:
            source = index_file.read().strip()
            client.indices.create(index=settings.INDEX_NAME, body=source)

        response = requests.post(
            url=settings.ENCODER_URL,
            json={'sentences': question_texts}
        )

        if response.status_code != 200:
            raise Exception('Encoder error')

        title_vectors = response.json()['vectors']

        elastic_requests = []

        for i, question in enumerate(question_texts):
            elastic_requests.append({
                'title': question,
                'title_vector': title_vectors[i],
                '_op_type': 'index',
                '_index': settings.INDEX_NAME
            })
        bulk(client, elastic_requests)
        client.indices.refresh(index=settings.INDEX_NAME)
