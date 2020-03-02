import json

from django.core.management.base import BaseCommand

from core.models import StepikUser


class Command(BaseCommand):
    help = 'Скрипт для импорта авторов комментариев из json'

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='?', type=str, default='../data/users.json')

    def handle(self, *args, **kwargs):
        with open(kwargs['json_file']) as file_obj:
            stepik_users_list = json.loads(file_obj.read())

        for stepik_user in stepik_users_list:
            try:
                StepikUser.objects.create(
                    id=stepik_user['id'],
                    full_name=stepik_user['full_name'],
                    avatar=stepik_user['avatar'],
                    level_title=stepik_user['level_title'],
                    knowledge=stepik_user['knowledge'],
                    reputation=stepik_user['reputation'],
                    solved_steps_count=stepik_user['reputation'],
                    issued_certificates_count=stepik_user['issued_certificates_count']
                )
            except Exception as e:
                print(e)
                continue
