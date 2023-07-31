from django.db import models
from config import settings

NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='заголовок')
    content = models.TextField(blank=True, verbose_name='содержимое')
    image = models.ImageField(upload_to='media/blog/', verbose_name='превью', **NULLABLE)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    is_public = models.BooleanField(default=True, verbose_name='публикация')
    num_views = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title} - {self.is_public}'

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Client(models.Model):
    email = models.EmailField(unique=True, verbose_name='почта')
    first_name = models.CharField(max_length=150, verbose_name='имя', **NULLABLE)
    last_name = models.CharField(max_length=150, verbose_name='фамилия', **NULLABLE)
    comment = models.TextField(max_length=255, verbose_name='комментарий', **NULLABLE)

    def __str__(self):
        return f'{self.first_name} {self.last_name}: {self.email}'

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Message(models.Model):
    title = models.CharField(max_length=60, verbose_name='тема письма')
    context = models.TextField(blank=True, verbose_name='текст письма')

    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, **NULLABLE,
                                verbose_name='создатель')

    def __str__(self):
        return f'сообщение {self.title}'

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Mailing(models.Model):
    TIME_CHOICES = (
        ('hourly', 'раз в час'),
        ('daily', 'раз в день'),
        ('weekly', 'раз в неделю'),
        ('monthly', 'раз в месяц'),
    )
    STATUS_CHOICES = (
        ('created', 'создана'),
        ('started', 'запущена'),
        ('completed', 'завершена'),
    )

    mailing_time = models.TimeField(verbose_name='время рассылки')
    periodicity = models.CharField(max_length=15, choices=TIME_CHOICES, verbose_name='периодичность')
    mailing_status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='created',
        verbose_name='статус рассылки'
    )
    is_active = models.BooleanField(default=False, verbose_name='рассылка активна')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, **NULLABLE)
    client = models.ManyToManyField('Client',
                                    verbose_name='клиент')

    def __str__(self):
        return f'{self.periodicity}, {self.mailing_status}: {self.is_active}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'


class LogiMail(models.Model):
    date_last = models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')
    status = models.BooleanField(default=False, verbose_name='статус попытки')
    server_answer = models.TextField(verbose_name='ответ почтового сервера', **NULLABLE)
    mailing = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='сообщение', **NULLABLE)

    def __str__(self):
        return f'{self.date_last}: {self.status}'

    class Meta:
        verbose_name = 'логи рассылки'