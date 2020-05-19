from django.db import models


class CourseMaterial(models.Model):
    course_id = models.PositiveIntegerField(
        verbose_name='Идентификатор курса',
        default=0
    )

    lesson_name = models.CharField(
        verbose_name='Название урока',
        max_length=255
    )

    section_id = models.PositiveIntegerField(
        verbose_name='Идентификатор раздела',
        default=0
    )

    lesson_id = models.PositiveIntegerField(
        verbose_name='Идентификатор урока',
        default=0
    )

    step_id = models.PositiveIntegerField(
        verbose_name='Идентификатор степа',
        default=0
    )

    stepik_link = models.CharField(
        verbose_name='Ссылка на страницу материала на Stepik',
        max_length=500
    )

    material_type = models.CharField(
        verbose_name='Тип материала',
        max_length=50,
        default='text'
    )

    text = models.TextField(
        verbose_name='Текст урока'
    )

    created_at = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True
    )

    objects = models.Manager()

    def __str__(self):
        return f"{self.lesson_name}: Раздел {self.section_id}, урок {self.lesson_id}, степ {self.step_id}, {self.material_type}"

    class Meta:
        verbose_name = 'Материал курса'
        verbose_name_plural = 'Материалы курса'
        ordering = ['created_at']
