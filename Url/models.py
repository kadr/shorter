import string
from random import choice

from django.db import models

from User.models import User


def generate_key():
    """Генерация случайного набора из 3 символов"""
    chars = string.digits + string.ascii_letters
    print(chars)
    return ''.join(choice(chars) for _ in range(3))


class Url(models.Model):
    """Ссылки"""

    session = ''
    ip = ''
    user_agent = ''
    referer = ''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='urls',
        verbose_name='Пользователь',
        default=None,
        null=True
    )
    short = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='Коротная ссылка'
    )
    full = models.CharField(
        max_length=255,
        default='',
        verbose_name='Полная ссылка'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Создан"
    )

    class Meta:
        ordering = ['user']
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    def __str__(self):
        return self.short

    def save(self, *args, **kwargs):
        if self.full:
            self.short = generate_key()
        super().save()


class Hit(models.Model):
    """Информация о кликах по укороченной ссылке"""

    ip = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='IP адрес'
    )
    click_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата клика"
    )
    user_agent = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='User Agent'
    )
    referer = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Referer'
    )
    url = models.ForeignKey(
        Url,
        on_delete=models.CASCADE,
        verbose_name='Ссылка',
        related_name='hits'
    )

    class Meta:
        ordering = ['click_date']
        verbose_name = 'Доп информация'
        verbose_name_plural = 'Доп информации'

    def __str__(self):
        return self.url.short
