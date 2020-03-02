from django.db import models


class Comment(models.Model):
    id = models.PositiveIntegerField(
        verbose_name='Идентификатор',
        unique=True,
        primary_key=True
    )

    parent = models.ForeignKey(
        verbose_name='Родительский комментарий',
        to='core.Comment',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    user_role = models.CharField(
        verbose_name='Роль комментатора',
        max_length=50,
        default='student'
    )

    text = models.TextField(
        verbose_name='Текст комментария'
    )

    epic_count = models.PositiveIntegerField(
        verbose_name='Количество лайков за комментарий',
        default=0
    )

    abuse_count = models.PositiveIntegerField(
        verbose_name='Количество дизлайков за комментарий',
        default=0
    )

    target = models.PositiveIntegerField(
        verbose_name='Идентификатор степа',
        default=0
    )

    user = models.ForeignKey(
        verbose_name='Автор комментария',
        to='core.StepikUser',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True
    )

    objects = models.Manager()

    def __str__(self):
        return self.text[:255]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
