# Generated by Django 4.2.2 on 2023-06-10 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('match', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='liker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liking', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='match',
            name='liking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likers', to=settings.AUTH_USER_MODEL),
        ),
    ]
