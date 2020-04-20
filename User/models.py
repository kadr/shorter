from django.db import models


class User(models.Model):
    """Класс хранения пользователей"""

    session_id = models.CharField(
        max_length=255,
        default=0,
        verbose_name='ID сессии пользователя'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан"
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.session_id
