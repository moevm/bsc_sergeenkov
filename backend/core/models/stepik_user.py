from django.db import models


class StepikUser(models.Model):
    id = models.PositiveIntegerField(
        verbose_name='Идентификатор',
        unique=True,
        primary_key=True
    )

    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=255
    )

    avatar = models.CharField(
        verbose_name='Аватар',
        max_length=500
    )

    level_title = models.CharField(
        verbose_name='Уровень',
        max_length=255
    )

    knowledge = models.PositiveIntegerField(
        verbose_name='Уровень знаний',
        default=0
    )

    reputation = models.PositiveIntegerField(
        verbose_name='Уровень репутации',
        default=0
    )

    solved_steps_count = models.PositiveIntegerField(
        verbose_name='Пройдено степов',
        default=0
    )

    issued_certificates_count = models.PositiveIntegerField(
        verbose_name='Получено сертификатов',
        default=0
    )

    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True
    )

    objects = models.Manager()

    class Meta:
        verbose_name = 'Автор комментария'
        verbose_name_plural = 'Авторы комментариев'
        ordering = ['-created_at']
