# Generated by Django 3.0.3 on 2020-05-19 08:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200519_1119'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursematerial',
            options={'ordering': ['created_at'], 'verbose_name': 'Материал курса', 'verbose_name_plural': 'Материалы курса'},
        ),
    ]
