import json

from django.core.management.base import BaseCommand

from core.models import CourseMaterial


class Command(BaseCommand):
    help = 'Скрипт для импорта материалов курса из json'

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='?', type=str, default='../data/course_materials.json')

    def handle(self, *args, **kwargs):
        with open(kwargs['json_file']) as file_obj:
            course_materials_list = json.loads(file_obj.read())
            for item_first_level in course_materials_list:
                for item_second_level in item_first_level:
                    for course_material in item_second_level:
                        print(course_material)
                        if course_material['content']:
                            try:
                                CourseMaterial.objects.create(
                                    lesson_name=course_material['lesson_name'],
                                    lesson_id=course_material['lesson_id'],
                                    step_id=course_material['step_id'],
                                    stepik_link=course_material['url'],
                                    material_type=course_material['type'],
                                    text=course_material['content']
                                )
                            except Exception as e:
                                print(e)
                                continue
