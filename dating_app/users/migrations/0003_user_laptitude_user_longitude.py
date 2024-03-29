# Generated by Django 4.2.2 on 2023-06-11 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_managers_alter_user_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='laptitude',
            field=models.FloatField(default=54.9827385, help_text='Укажите широту вашего местоположения', verbose_name='Широта'),
        ),
        migrations.AddField(
            model_name='user',
            name='longitude',
            field=models.FloatField(default=82.8977945, help_text='Укажите долготу вашего местоположения', verbose_name='Долготу'),
        ),
    ]
