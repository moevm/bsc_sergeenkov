# Generated by Django 3.0.3 on 2020-05-19 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_coursematerial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursematerial',
            name='lesson_name',
            field=models.CharField(default='lesson', max_length=255, verbose_name='Название урока'),
            preserve_default=False,
        ),
    ]
