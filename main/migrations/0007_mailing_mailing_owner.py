# Generated by Django 4.2.3 on 2023-08-04 22:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0006_client_client_owner_client_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailing',
            name='mailing_owner',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Создатель рассылки'),
        ),
    ]
