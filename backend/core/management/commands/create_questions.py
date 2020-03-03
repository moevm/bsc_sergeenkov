from django.core.management.base import BaseCommand

from core.models import (
    Comment,
    Question
)


class Command(BaseCommand):
    help = 'Скрипт для извлечения вопросительных комментариев'

    def handle(self, *args, **kwargs):
        comments = Comment.objects.filter(parent=None)

        for comment in comments:
            if len(comment.text) > 10:
                Question.objects.create(question=comment.text)
