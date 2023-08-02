from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):

    USER_STATUS = [
        (True, 'Активирован'),
        (False, 'Не активирован')
    ]

    username = None

    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)

    email_verify = models.BooleanField(default=False)
    verification_key = models.CharField(default='Не верифицирован', verbose_name='Ключ активации')
    is_active = models.BooleanField(default=False, verbose_name='Статус активации')


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'