from django.db import models


class Answer(models.Model):
    answer_type = models.CharField(
        verbose_name='Тип ответа',
        max_length=100,
        default='course_material'
    )

    question = models.ForeignKey(
        verbose_name='Вопрос',
        to='core.Question',
        on_delete=models.CASCADE
    )

    course_material = models.ForeignKey(
        verbose_name='Материал курса',
        to='core.CourseMaterial',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    comment = models.ForeignKey(
        verbose_name='Комментарий',
        to='core.Comment',
        blank=True,
        null=True,
        on_delete=models.DO_NOTHING
    )

    content = models.TextField(
        verbose_name='Текст ответа',
        blank=True,
        null=True
    )

    votes = models.PositiveIntegerField(
        verbose_name='Количество голосов',
        default=1
    )

    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True
    )

    objects = models.Manager()

    class Meta:
        verbose_name = 'Ответ на вопрос'
        verbose_name_plural = 'Ответы на вопросы'
        ordering = ['created_at']
