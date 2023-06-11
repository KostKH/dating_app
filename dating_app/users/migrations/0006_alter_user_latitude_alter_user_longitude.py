# Generated by Django 4.2.2 on 2023-06-11 10:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_user_laptitude_between_minus90_90_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='latitude',
            field=models.FloatField(default=54.9827385, help_text='Укажите широту вашего местоположения', validators=[django.core.validators.MinValueValidator(-90.0, message='Должно быть значение от -90.000000 до 90.000000'), django.core.validators.MaxValueValidator(90.0, message='Должно быть значение от -90.000000 до 90.000000')], verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='user',
            name='longitude',
            field=models.FloatField(default=82.8977945, help_text='Укажите долготу вашего местоположения', validators=[django.core.validators.MinValueValidator(-180.0, message='Должно быть значение от -180.00000 до 180.000000'), django.core.validators.MaxValueValidator(180.0, message='Должно быть значение от -180.000000 до 180.000000')], verbose_name='Долгота'),
        ),
    ]
