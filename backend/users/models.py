from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=255,
        blank=True,
        null=True
    )

    avatar = models.CharField(
        verbose_name='Аватар',
        max_length=500,
        blank=True,
        null=True
    )

    stepik_id = models.PositiveIntegerField(
        verbose_name='Идентификатор пользователя на Stepik',
        default=0
    )

    user = models.OneToOneField(
        verbose_name='Пользователь для авторизации',
        to=User,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True
    )

    objects = models.Manager()

    @property
    def url(self):
        return f'https://stepik.org/users/{self.stepik_id}'

    class Meta:
        app_label = 'users'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили пользователей'
        ordering = ['created_at']


# Создание профиля ползователя сразу после создания нового юзера
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

