from django.db import models


class Question(models.Model):
    question = models.TextField(
        verbose_name='Вопрос'
    )

    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True
    )

    objects = models.Manager()

    def __str__(self):
        return self.questions

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['-created_at']
