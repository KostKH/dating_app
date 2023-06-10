from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Match(models.Model):
    """Класс Match создает БД SQL для хранения
    информации о Симпатиях пользователей друг к другу"""

    liker = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='liking'
    )
    liking = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='likers'
    )

    class Meta:

        constraints = [
            models.UniqueConstraint(
                fields=['liker', 'liking'],
                name='unique_liker_liking'
            )
        ]
        verbose_name = 'Симпатии пользователей'
        verbose_name_plural = 'Симпатии пользователей'

    def __str__(self):
        liker_str = str(self.liker.email)
        liking_str = str(self.liking.email)
        return liker_str + ' - ' + liking_str
