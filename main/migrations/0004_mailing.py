

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailing_time', models.TimeField(verbose_name='время рассылки')),
                ('periodicity', models.CharField(choices=[('hourly', 'раз в час'), ('daily', 'раз в день'), ('weekly', 'раз в неделю'), ('monthly', 'раз в месяц')], max_length=15, verbose_name='периодичность')),
                ('mailing_status', models.CharField(choices=[('created', 'создана'), ('started', 'запущена'), ('completed', 'завершена')], default='created', max_length=15, verbose_name='статус рассылки')),
                ('is_active', models.BooleanField(default=False, verbose_name='рассылка активна')),
                ('client', models.ManyToManyField(to='main.client', verbose_name='клиент')),
                ('message', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.message')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
    ]
