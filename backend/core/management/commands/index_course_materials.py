import requests

from django.core.management.base import BaseCommand

from django.conf import settings

from core.models import CourseMaterial

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class Command(BaseCommand):
    help = 'Скрипт для индексирования материалов курса в ES'

    def handle(self, *args, **kwargs):
        course_materials = CourseMaterial.objects.all()
        course_materials_texts = [course_material.text for course_material in course_materials]

        client = Elasticsearch(settings.ELASTICSEARCH_URL)
        client.indices.delete(index=settings.COURSE_MATERIALS_INDEX_NAME, ignore=[404])
        with open(settings.COURSE_MATERIALS_INDEX_FILE) as index_file:
            source = index_file.read().strip()
            client.indices.create(index=settings.COURSE_MATERIALS_INDEX_NAME, body=source)

        response = requests.post(
            url=settings.ENCODER_URL,
            json={'sentences': course_materials_texts}
        )

        if response.status_code != 200:
            raise Exception('Encoder error')

        text_vectors = response.json()['vectors']

        elastic_requests = []

        for i, text in enumerate(course_materials_texts):
            print(f'Appending {course_materials[i].lesson_name}')
            elastic_requests.append({
                'content': text,
                'content_vector': text_vectors[i],
                'django_id': str(course_materials[i].id),
                'course_id': course_materials[i].course_id,
                'lesson_name': course_materials[i].lesson_name,
                'section_id': course_materials[i].section_id,
                'lesson_id': course_materials[i].lesson_id,
                'step_id': course_materials[i].step_id,
                'url': course_materials[i].stepik_link,
                '_op_type': 'index',
                '_index': settings.COURSE_MATERIALS_INDEX_NAME
            })
        bulk(client, elastic_requests)
        client.indices.refresh(index=settings.COURSE_MATERIALS_INDEX_NAME)
