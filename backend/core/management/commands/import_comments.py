import json
import re

from django.core.management.base import BaseCommand

from core.models import (
    Comment,
    StepikUser
)

TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub(' ', text).strip()


class Command(BaseCommand):
    help = 'Скрипт для импорта комментариев из json'

    def add_arguments(self, parser):
        parser.add_argument('json_file', nargs='?', type=str, default='../data/comments.json')

    def handle(self, *args, **kwargs):
        with open(kwargs['json_file']) as file_obj:
            comments_list = json.loads(file_obj.read())

        # Первый проход - просто создаем комментарии
        for comment in comments_list:
            try:
                try:
                    stepik_user = StepikUser.objects.get(id=comment['user'])
                except StepikUser.DoesNotExist:
                    stepik_user = None
                Comment.objects.create(
                    id=comment['id'],
                    user_role=comment['user_role'],
                    text=remove_tags(comment['text']),
                    epic_count=comment['epic_count'],
                    abuse_count=comment['abuse_count'],
                    target=comment['target'],
                    user=stepik_user
                )
            except Exception as e:
                print(e)
                continue

        # Второй проход - связываем родительские и дочерние комментарии
        for comment in comments_list:
            if comment['parent']:
                try:
                    parent_comment = Comment.objects.get(id=comment['parent'])
                    child_comment = Comment.objects.get(id=comment['id'])
                    child_comment.parent = parent_comment
                    child_comment.save()
                except Comment.DoesNotExist:
                    continue

