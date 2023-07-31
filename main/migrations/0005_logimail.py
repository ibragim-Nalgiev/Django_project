

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_mailing'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogiMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_last', models.DateTimeField(auto_now=True, verbose_name='дата и время последней попытки')),
                ('status', models.BooleanField(default=False, verbose_name='статус попытки')),
                ('server_answer', models.TextField(blank=True, null=True, verbose_name='ответ почтового сервера')),
                ('mailing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.mailing', verbose_name='сообщение')),
            ],
            options={
                'verbose_name': 'логи рассылки',
            },
        ),
    ]
